import asyncio
from collections import defaultdict

from csv import Error
from dataclasses import dataclass, field
import heapq
import itertools
from typing import Any, Generic, List, Literal,  TypeVar, Callable

from mp_async_worker.async_worker import AsyncWorker





@dataclass(order=True)
class PrioritizedItem:
    priority: int
    count: int
    task :int
    item: Any=field(compare=False)


B = TypeVar('B') # Arguments
R = TypeVar('R') #  results

class AsyncPriortyBatchWorker(Generic[B,R]):
    
    priorityQueue:List[PrioritizedItem] =[]
    _counter = itertools.count()
    _task_counter = itertools.count()
    _results = defaultdict(list)
    def __init__(
        self,
                 task:Callable[[B],R],
        batch_size: int = 32
        ):
        
        self.worker:AsyncWorker = AsyncWorker(task)
        self.batch_size = batch_size 

    def start(self):
        self.worker.start()
    
    def stop(self):
        self.worker.stop()

    def _get_mini_batch(self) -> List[PrioritizedItem]:
        counter = 0
        mini_batch = [None] * min(self.batch_size,len(self.priorityQueue))
        while counter < self.batch_size and len(self.priorityQueue) >0:
            mini_batch[counter] = heapq.heappop(self.priorityQueue) # type: ignore
            counter += 1
        return mini_batch # type: ignore
    
    async def run(self, batch:List[B], *args,priority=10 ) -> List[R]:
        """
        Runs a batch of tasks asynchronously, ensuring one result per input.
        
        Args:
            batch (List[B]): List of input items to be processed.
            priority (int, optional): Priority level of the batch (default: 10). Smaller == higher priority
        
        Returns:
            List[R]: The results corresponding to the input batch.
        
        Raises:
            Exception: If the number of results does not match the number of inputs.
        """
        task_id = next(self._task_counter)
        for item in batch:
            heapq.heappush(self.priorityQueue,PrioritizedItem(priority,next(self._counter),task_id,item))
        
        done = False
        while len(self.priorityQueue) >0 and not done:
            mini_batch = self._get_mini_batch()
            results = await self.worker.run([i.item for i in mini_batch],*args)
            # print(f'Batch prios {[b.task for b in mini_batch]} done.')
            if isinstance(results,Exception):
                raise results
            for b,r in zip(mini_batch,results):
                self._results[b.task].append(r)
                if not done and len(self._results[task_id]) == len(batch):
                    done = True     
        if len(self._results[task_id]) != len(batch):
            await asyncio.sleep(1)
            if len(self._results[task_id]) != len(batch):
                raise Exception("It seems the task has not returned the same number of results.")
        return self._results[task_id]
