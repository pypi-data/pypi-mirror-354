

import asyncio
import pytest

from mp_async_worker import AsyncWorker
from tasks import batch_task, error_batch_task, item_task, multiarg_batch_task

@pytest.mark.asyncio
async def test_multiarg():
    worker = AsyncWorker(multiarg_batch_task)
    worker.start()
    result = await worker.run([5], 2)
    worker.stop()
    assert result == [5]

@pytest.mark.asyncio
async def test_multiarg_wrong_arg():
    worker = AsyncWorker(multiarg_batch_task)
    worker.start()
    with pytest.raises(TypeError):
        result = await worker.run(5, 2)
    worker.stop()

@pytest.mark.asyncio    
async def test_item():
    worker = AsyncWorker(item_task)
    worker.start()
    result = await worker.run(5)
    worker.stop()
    assert result == 5*6

@pytest.mark.asyncio    
async def test_item_wrong_args():
    worker = AsyncWorker(item_task)
    worker.start()
    with pytest.raises(TypeError):
        result = await worker.run(5,2)
    worker.stop()

@pytest.mark.asyncio
async def test_sync():
    worker = AsyncWorker(batch_task)
    worker.start()
    result = await worker.run([5])
    worker.stop()
    assert result == [25]

@pytest.mark.asyncio
async def test_error():
    worker = AsyncWorker(error_batch_task)
    worker.start()
    with pytest.raises(ValueError, match="Intentional error"):
        await worker.run([1, 2, 3])
    worker.stop()
    

@pytest.mark.asyncio
async def test_async_worker():
    worker = AsyncWorker(batch_task)
    worker.start()

    future1 = worker.run([5])
    future2 = worker.run([-53])
    result1 = await future1
    result2 = await future2
    assert result1 == [25]
    assert result2 == [2809]

    futures = [worker.run([i * i]) for i in range(20)]
    results = [await f for f in futures]
    expected_results = [[(i * i) * (i * i)] for i in range(20)]
    assert results == expected_results

    futures = [worker.run([i]) for i in range(20)]
    gathered_results = await asyncio.gather(*futures)
    expected_gathered = [[i * i] for i in range(20)]
    assert gathered_results == expected_gathered

    worker.stop()


