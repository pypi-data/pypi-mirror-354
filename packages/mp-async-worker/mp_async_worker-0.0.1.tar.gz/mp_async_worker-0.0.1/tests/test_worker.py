import pytest

from mp_async_worker import Worker
from tasks import batch_task, error_batch_task, item_task, multiarg_batch_task

def test_multiarg():
    worker = Worker(multiarg_batch_task)
    worker.start()
    result = worker.run([5], 2)
    worker.stop()
    assert result == [5]

def test_multiarg_wrong_arg():
    worker = Worker(multiarg_batch_task)
    worker.start()
    with pytest.raises(TypeError):
        result = worker.run(5, 2)
    worker.stop()
    
def test_item():
    worker = Worker(item_task)
    worker.start()
    result = worker.run(5)
    worker.stop()
    assert result == 5*6
    
def test_item_wrong_args():
    worker = Worker(item_task)
    worker.start()
    with pytest.raises(TypeError):
        result = worker.run(5,2)
    worker.stop()

def test_sync():
    worker = Worker(batch_task)
    worker.start()
    result = worker.run([5])
    worker.stop()
    assert result == [25]

def test_error():
    worker = Worker(error_batch_task)
    worker.start()
    with pytest.raises(ValueError, match="Intentional error"):
        worker.run([1, 2, 3])
    worker.stop()
    
