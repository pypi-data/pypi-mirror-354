import time

try:
    import redis.asyncio
    import redis.asyncio.client
    import redis.asyncio.lock
except ImportError as exc:
    raise ImportError(
        'The "redis" package is required for the Redis backend. '
        'Install it with: pip install "token-throttle[redis]"'
    ) from exc
from pydantic import BaseModel

from token_throttle._interfaces._interfaces import PerModelConfig
from token_throttle._interfaces._models import Quota


class CalculatedCapacity(BaseModel):
    amount: float
    is_fresh_start: bool


class RedisBucket:
    def __init__(
        self,
        quota: Quota,
        limit_config: PerModelConfig,
        redis_client: redis.asyncio.Redis,
    ):
        self.usage_metric = quota.metric
        self.per_seconds = float(quota.per_seconds)
        self.full_redis_key = f"rate_limiting:{limit_config.model_family}:{self.usage_metric}:{int(self.per_seconds)}"
        self.model_family = limit_config.get_model_family()
        self.max_capacity = float(quota.limit)

        self._redis = redis_client
        self._rate_per_sec = float(quota.limit) / float(quota.per_seconds)
        # Keys for Redis
        self._last_checked_key = f"{self.full_redis_key}:last_checked"
        self._capacity_key = f"{self.full_redis_key}:capacity"
        self._lock_key = f"{self.full_redis_key}:lock"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RedisBucket):
            return False
        return (
            self.usage_metric == other.usage_metric
            and self.full_redis_key == other.full_redis_key
            and self._rate_per_sec == other._rate_per_sec
            and self.max_capacity == other.max_capacity
            and self.per_seconds == other.per_seconds
            and self._last_checked_key == other._last_checked_key
            and self._capacity_key == other._capacity_key
            and self._lock_key == other._lock_key
        )

    def lock(self, **kwargs) -> redis.asyncio.lock.Lock:
        return redis.asyncio.lock.Lock(self._redis, self._lock_key, **kwargs)

    async def get_capacity(
        self,
        pipeline: redis.asyncio.client.Pipeline | None = None,
        current_time: float | None = None,
    ) -> CalculatedCapacity | None:
        """Get the current capacity of the bucket."""
        if current_time is None:
            current_time = time.time()

        own_pipeline = pipeline is None
        if own_pipeline:
            pipeline = self._redis.pipeline()

        pipeline.get(self._last_checked_key)
        pipeline.get(self._capacity_key)

        if own_pipeline:
            results = await pipeline.execute()
            last_checked, capacity = results
            return self.calculate_capacity(last_checked, capacity, current_time)
        return None

    async def set_capacity(
        self,
        new_capacity: float,
        pipeline: redis.asyncio.client.Pipeline | None = None,
        current_time: float | None = None,
        *,
        execute: bool = True,
    ) -> None:
        if current_time is None:
            current_time = time.time()

        own_pipeline = pipeline is None
        if own_pipeline:
            pipeline = self._redis.pipeline()

        new_capacity = max(0, new_capacity)
        pipeline.set(self._last_checked_key, current_time)
        pipeline.set(self._capacity_key, new_capacity)

        if execute and own_pipeline:
            await pipeline.execute()

    def calculate_capacity(
        self,
        last_checked,
        outdated_capacity,
        current_time: float,
    ) -> CalculatedCapacity:
        if last_checked is None or outdated_capacity is None:
            return CalculatedCapacity(amount=self.max_capacity, is_fresh_start=True)

        try:
            last_checked = float(last_checked)
            outdated_capacity = float(outdated_capacity)
        except (TypeError, ValueError) as e:
            raise ValueError(
                f"Invalid last_checked or capacity values: last_checked={last_checked}, capacity={outdated_capacity}",
            ) from e

        # Calculate new capacity with refill over time
        time_passed = current_time - last_checked
        current_preconsumption_capacity = min(
            self.max_capacity,
            outdated_capacity + time_passed * self._rate_per_sec,
        )
        return CalculatedCapacity(
            amount=current_preconsumption_capacity,
            is_fresh_start=False,
        )
