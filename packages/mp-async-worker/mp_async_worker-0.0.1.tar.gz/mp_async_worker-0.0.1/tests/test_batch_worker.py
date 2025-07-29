import asyncio
import pytest
from typing import List

from mp_async_worker.async_priority_batch_worker import AsyncPriortyBatchWorker


def batch_div_zero_function(a: List[float]) -> List[float]:
    return [x /0 for x in a]

def batch_function(a: List[int]) -> List[int]:
    return [x * x for x in a]

import contextlib
from typing import Callable, Any, List

@contextlib.asynccontextmanager
async def async_priority_batch_context(task_func: Callable[[Any], Any]= batch_function, batch_size: int = 32):
    worker = AsyncPriortyBatchWorker(task_func, batch_size=batch_size)
    try:
        yield worker
    finally:
        if worker:
            worker.worker.stop()

@pytest.mark.asyncio
async def test_batch():
    async with async_priority_batch_context() as worker:
        batch = list(range(50))
        results = await worker.run(batch, priority=10)
        expected = [i * i for i in range(50)]
        assert len(results) == len(batch)
        assert results == expected


@pytest.mark.asyncio
async def test_priority_handling():
    async with async_priority_batch_context() as worker:
        # Submit two batches with different priorities
        high_batch = list(range(64))
        low_batch = list(range(642))  # Adjusted to have consistent batch sizes
        
        future_low = asyncio.create_task(worker.run(low_batch, priority=10))
        future_high = asyncio.create_task(worker.run(high_batch, priority=1))

        # Wait for the first future to complete
        done_set, pending = await asyncio.wait({future_high, future_low}, return_when=asyncio.FIRST_COMPLETED)
        
        if future_high in done_set:
            assert True, "High-priority task completed before low-priority task"
            
            # Check if future_low is still pending
            assert future_low not in done_set, "Low-priority task should still be running"
        else:
            assert False, "High-priority task did not complete first"

        # Now wait for the remaining futures to complete
        results = await asyncio.gather(*pending, return_exceptions=True)
        
        if len(pending) > 0:
            if future_low in pending:
                low_results = results[0]
                assert len(low_results) == len(low_batch), f"Expected {len(low_batch)} results, got {len(low_results)}" # type: ignore
                


@pytest.mark.asyncio
async def test_batch_size_handling():
    async with async_priority_batch_context() as worker:
        large_batch = list(range(100))
        
        results = await worker.run(large_batch, priority=10)
        
        assert len(results) == 100
        expected = [i * i for i in range(100)]
        assert results == expected


@pytest.mark.asyncio
async def test_error_handling():
    async with async_priority_batch_context(batch_div_zero_function,8) as error_worker:

        with pytest.raises(ZeroDivisionError):
            await error_worker.run([1,2,3])

        error_worker.worker.stop()



@pytest.mark.asyncio
async def test_empty_batch():
    async with async_priority_batch_context() as worker:

        worker = AsyncPriortyBatchWorker(batch_function, batch_size=32)
        
        empty_results = await worker.run([], priority=10)
        assert len(empty_results) == 0

