"""
pip install sentence_transformers 'fastapi[standard]'

A FastAPI server that demonstrates a priority-based, asynchronous batch worker
for sentence embedding. High-priority jobs are processed before low-priority ones.

To properly observe the priority mechanism, you need to send the high-priority
request *while* the low-priority one is still being processed.

The easiest way to simulate this is with two separate terminal windows:
1.  In your first terminal, paste and run the long low-priority command. It will start working, and your prompt will not return immediately.
2.  While the first terminal is still busy, open a second terminal and run the short high-priority command.

You will see the second terminal (high-priority) return a result almost instantly. This proves it jumped ahead of the much larger job still running in the first terminal.


curl -X POST http://localhost:8000/low_prio \
  -H "Content-Type: application/json" \
  -d "$(python3 -c 'import random, string, json; print(json.dumps(["".join(random.choices(string.ascii_letters + string.digits, k=random.randint(1,50))) for _ in range(1000)]))')"

curl -X POST http://localhost:8000/high_prio \
  -H "Content-Type: application/json" \
  -d '["System failure imminent.", "Reboot protocol engaged.", "Notify administrator immediately."]'

"""
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI
from mp_async_worker import AsyncPriortyBatchWorker

_model = None
def _get_model():
    from sentence_transformers import SentenceTransformer
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2") 
        return _model
    return _model

    

def task(batch:List[str]):
    import numpy as np 
    from sentence_transformers import SentenceTransformer
    model = _get_model()
    embeddings = model.encode(batch)
    return np.stack(embeddings)[:,:3].tolist()


_batch_worker = None
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    global _batch_worker
    _batch_worker = AsyncPriortyBatchWorker(task,8)
    _batch_worker.start()
    yield
    _batch_worker.stop()

app = FastAPI(
    lifespan= lifespan
)
@app.post("/low_prio")
async def low_prio(batch: List[str]):
    assert _batch_worker
    return await _batch_worker.run(batch,priority=20)



@app.post("/high_prio")
async def high_prio(batch: List[str]):
    assert _batch_worker
    return await _batch_worker.run(batch,priority=2)