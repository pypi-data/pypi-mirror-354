import uuid
import time
import threading
from contextlib import contextmanager
from redis import Redis, RedisCluster
from redis.exceptions import LockError, TimeoutError
import logging

logger = logging.getLogger(__name__)

class RedisSemaphore:
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

    @contextmanager
    def acquire(self):
        lease_id = self.acquire_lease()
        try:
            yield
        finally:
            self.release_lease(lease_id)

    def acquire_lease(self) -> str:
        lease_id = str(uuid.uuid4())
        start_time = time.time()

        if self._try_acquire(lease_id):
            return lease_id

        self._join_waiting_queue(lease_id)

        while True:
            elapsed = time.time() - start_time
            if elapsed > self.wait_timeout:
                self._remove_from_waiting(lease_id)
                raise TimeoutError("Timeout acquiring semaphore")

            position = self.redis.zrank(self._waiting_zset, lease_id)
            if position is None:
                raise LockError("Lease ID unexpectedly removed from waiting queue")

            if position < self.max_concurrency:
                if self._try_acquire(lease_id):
                    self._remove_from_waiting(lease_id)
                    return lease_id

            time.sleep(0.5)

    def _try_acquire(self, lease_id: str) -> bool:
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
        result = self.redis.eval(
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

    def release_lease(self, lease_id: str):
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
        self.redis.eval(
            lua_script,
            2,
            self._counter_key,
            self._leases_key,
            lease_id
        )

    def _join_waiting_queue(self, lease_id: str):
        score = int(time.time() * 1000)
        self.redis.zadd(self._waiting_zset, {lease_id: score})

    def _remove_from_waiting(self, lease_id: str):
        self.redis.zrem(self._waiting_zset, lease_id)

    def start_cleanup_task(self, interval: float = 30.0):
        def _run():
            while True:
                try:
                    self._cleanup_expired_leases()
                except Exception as e:
                    logger.error(f"[Semaphore Cleanup Error] {e}")
                time.sleep(interval)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()

    def _cleanup_expired_leases(self):
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
        self.redis.eval(
            lua_script,
            2,
            self._counter_key,
            self._leases_key,
            str(int(time.time()))
        )
