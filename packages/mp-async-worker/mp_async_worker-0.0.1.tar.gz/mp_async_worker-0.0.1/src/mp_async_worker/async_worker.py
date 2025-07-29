import asyncio
from collections.abc import Callable

from mp_async_worker.worker import R, Worker




class AsyncWorker(Worker):
    def __init__(self, task: Callable) -> None:
        super().__init__(task)
        self._futures: dict[int, asyncio.Future] = {}
        self._request_id = 0  # Unique ID per request
        self._loop = asyncio.get_event_loop()
        self._loop.add_reader(self.connection.fileno(), self._read_from_connection)


    def _read_from_connection(self):
        try:
            request_id, result = self.connection.recv()
            if request_id in self._futures:
                future = self._futures.pop(request_id)
                if isinstance(result, Exception):
                    self._loop.call_soon_threadsafe(future.set_exception, result)
                else:
                    self._loop.call_soon_threadsafe(future.set_result, result)
        except Exception as e:
            for future in self._futures.values():
                self._loop.call_soon_threadsafe(future.set_exception, e)


    async def run(self, *args) -> R:
        future = self._loop.create_future()
        self._request_id += 1
        self._futures[self._request_id] = future
        self.connection.send((self._request_id, args))  # Send request with ID
        return await future