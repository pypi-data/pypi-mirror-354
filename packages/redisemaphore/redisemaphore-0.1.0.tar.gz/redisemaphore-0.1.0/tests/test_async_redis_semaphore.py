import asyncio
import pytest
import time
from redis.asyncio import Redis
from redisemaphore import AsyncRedisSemaphore

@pytest.fixture(scope="module")
async def redis_client():
    client = Redis(host="localhost", port=6379, decode_responses=True)
    await client.flushdb()
    yield client
    await client.flushdb()
    await client.close()

@pytest.mark.asyncio
async def test_acquire_and_release(redis_client):
    semaphore = AsyncRedisSemaphore(redis_client, "test_async", max_concurrency=2, lease_time=5, wait_timeout=5)

    async with semaphore.acquire():
        current = int(await redis_client.get(semaphore._counter_key) or 0)
        assert current == 1

    current_after = int(await redis_client.get(semaphore._counter_key) or 0)
    assert current_after == 0

@pytest.mark.asyncio
async def test_concurrent_limit_timeout(redis_client):
    semaphore = AsyncRedisSemaphore(redis_client, "test_async_limit", max_concurrency=1, lease_time=1, wait_timeout=1)

    lease1 = await semaphore.acquire_lease()

    start = time.time()
    with pytest.raises(asyncio.TimeoutError):
        await semaphore.acquire_lease()
    elapsed = time.time() - start
    assert elapsed >= 1

    await semaphore.release_lease(lease1)
