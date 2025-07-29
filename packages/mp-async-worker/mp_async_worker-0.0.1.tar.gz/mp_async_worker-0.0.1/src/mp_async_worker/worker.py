import asyncio
from collections.abc import Callable
from concurrent.futures import Future
import multiprocessing as mp
from multiprocessing import Process
from multiprocessing.connection import Connection
from typing import TypeVar

try:
    from typing import ParamSpec  # Python 3.10+
except ImportError:
    from typing_extensions import ParamSpec  # Python <3.10


A = ParamSpec('A') # Arguments
R = TypeVar('R') #  results

def _runner(connection: Connection, f: Callable):
    eof = False
    while not eof:
        request_id=-1
        try:
            request_id, task_args = connection.recv()  # Expecting (id, args)
            results = f(*task_args)
            connection.send((request_id, results))  # Send with request ID
        except EOFError:
            eof = True
        except Exception as e:
            # eof = True
            connection.send((request_id, e))  # Send exception with ID
    connection.close()

class Worker:
    task:Callable
    def __init__(self,
                 task:Callable
                 ) -> None:
        parent_conn, child_conn = mp.Pipe()
        mp.set_start_method("spawn", force=True) 
        self.process =  Process(target=_runner, args=[child_conn,task])
        self.connection = parent_conn
        self.task= task
        self.running=False
        
    
    def start(self):
        self.process.start()
        self.running=True
        
    def stop(self):
        self.connection.close()
        self.process.terminate()
        self.running=False
    
    def run(self,*args) -> R:
        self.connection.send((0,args))
        result = self.connection.recv()[1]
        if isinstance(result,Exception):
            raise result
        return result
    



