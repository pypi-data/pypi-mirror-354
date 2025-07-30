import asyncio
import uuid
import time
from contextlib import asynccontextmanager
from redis.asyncio import Redis, RedisCluster
from redis.exceptions import LockError
import logging

logger = logging.getLogger(__name__)

class AsyncRedisSemaphore:
    def __init__(
        self,
        redis: Redis | RedisCluster,
        semaphore_name: str,
        max_concurrency: int,
        lease_time: float = 30.0,
        wait_timeout: float = 60.0,
    ):
        self.redis = redis
        self.semaphore_name = semaphore_name
        self.max_concurrency = max_concurrency
        self.lease_time = lease_time
        self.wait_timeout = wait_timeout
        self._base_key = f"semaphore:{{{semaphore_name}}}"

        self._counter_key = f"{self._base_key}:counter"
        self._leases_key = f"{self._base_key}:leases"
        self._waiting_zset = f"{self._base_key}:waiting"

    @asynccontextmanager
    async def acquire(self):
        lease_id = await self.acquire_lease()
        try:
            yield
        finally:
            await self.release_lease(lease_id)


    async def acquire_lease(self) -> str:
        lease_id = str(uuid.uuid4())
        start_time = time.time()

        if await self._try_acquire(lease_id):
            return lease_id

        await self._join_waiting_queue(lease_id)

        while True:
            elapsed = time.time() - start_time
            if elapsed > self.wait_timeout:
                await self._remove_from_waiting(lease_id)
                raise asyncio.TimeoutError("Timeout acquiring semaphore")

            position = await self.redis.zrank(self._waiting_zset, lease_id)
            if position is None:
                raise LockError("Lease ID unexpectedly removed from waiting queue")

            if position < self.max_concurrency:
                if await self._try_acquire(lease_id):
                    await self._remove_from_waiting(lease_id)
                    return lease_id

            await asyncio.sleep(0.5)

    async def _try_acquire(self, lease_id: str) -> bool:
        """
        Tries to acquire a lease if under the concurrency limit.
        Stores lease with an expiration timestamp.
        """
        current_time = int(time.time())
        expire_time = current_time + int(self.lease_time)

        lua_script = """
        local counter_key = KEYS[1]
        local leases_key = KEYS[2]
        local max_concurrent = tonumber(ARGV[1])
        local lease_id = ARGV[2]
        local expire_time = ARGV[3]

        local current = tonumber(redis.call('GET', counter_key) or "0")
        if current < max_concurrent then
            redis.call('INCR', counter_key)
            redis.call('HSET', leases_key, lease_id, expire_time)
            redis.call('EXPIRE', leases_key, tonumber(ARGV[4]))
            return 1
        else
            return 0
        end
        """
        result = await self.redis.eval(
            lua_script,
            2,
            self._counter_key,
            self._leases_key,
            str(self.max_concurrency),
            lease_id,
            str(expire_time),
            str(int(self.lease_time) * 2),
        )
        return bool(result)

    async def release_lease(self, lease_id: str):
        lua_script = """
        local counter_key = KEYS[1]
        local leases_key = KEYS[2]
        local lease_id = ARGV[1]

        if redis.call('HEXISTS', leases_key, lease_id) == 1 then
            redis.call('HDEL', leases_key, lease_id)
            redis.call('DECR', counter_key)
            return 1
        else
            return 0
        end
        """
        await self.redis.eval(
            lua_script,
            2,
            self._counter_key,
            self._leases_key,
            lease_id
        )

    async def _join_waiting_queue(self, lease_id: str):
        score = int(time.time() * 1000)
        await self.redis.zadd(self._waiting_zset, {lease_id: score})

    async def _remove_from_waiting(self, lease_id: str):
        await self.redis.zrem(self._waiting_zset, lease_id)

    async def start_cleanup_task(self, interval: float = 30.0):
        while True:
            await self._cleanup_expired_leases()
            await asyncio.sleep(interval)

    async def _cleanup_expired_leases(self):
        lua_script = """
        local counter_key = KEYS[1]
        local leases_key = KEYS[2]
        local current_time = tonumber(ARGV[1])

        local all_leases = redis.call('HGETALL', leases_key)
        local valid_leases = {}
        local count = 0

        for i = 1, #all_leases, 2 do
            local lease_id = all_leases[i]
            local expire_time = tonumber(all_leases[i + 1])
            if expire_time and expire_time > current_time then
                table.insert(valid_leases, lease_id)
                table.insert(valid_leases, expire_time)
                count = count + 1
            end
        end

        redis.call('DEL', leases_key)
        for i = 1, #valid_leases, 2 do
            redis.call('HSET', leases_key, valid_leases[i], valid_leases[i + 1])
        end
        redis.call('SET', counter_key, tostring(count))
        return count
        """
        try:
            await self.redis.eval(
                lua_script,
                2,
                self._counter_key,
                self._leases_key,
                str(int(time.time()))
            )
        except Exception as e:
            logger.error(f"[Semaphore Cleanup Error] {e}")
