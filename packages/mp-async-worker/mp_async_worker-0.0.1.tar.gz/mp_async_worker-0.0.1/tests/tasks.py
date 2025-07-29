
from typing import List


def multiarg_batch_task(a: List[int], batch_size: int) -> List[int]:
    ret = []
    for item in a:
        ret.append( item)
    return ret

def batch_task(a: List[int]) -> List[int]:
    return [x * x for x in a]

def item_task(item:int) -> int:
    return item*6

def error_batch_task(a: List[int]) -> List[int]:
    raise ValueError("Intentional error")
