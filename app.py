from fastapi import FastAPI, HTTPException, Body
from typing import Dict, Any, Optional
from models import WarehouseAction, WarehouseObservation, WarehouseReward, WarehouseState
from environment import WarehouseEnv

app = FastAPI()

# In-memory store for environments (Simplified for HF Spaces deployment)
envs: Dict[str, WarehouseEnv] = {}

def get_env(task_id: str = "schema_drift") -> WarehouseEnv:
    if task_id not in envs:
        envs[task_id] = WarehouseEnv(task_id=task_id)
    return envs[task_id]

@app.post("/reset", response_model=WarehouseObservation)
async def reset(task_id: str = Body("schema_drift", embed=True)):
    env = get_env(task_id)
    return await env.reset()

@app.post("/step", response_model=WarehouseReward)
async def step(action: WarehouseAction, task_id: str = Body("schema_drift", embed=True)):
    env = get_env(task_id)
    return await env.step(action)

@app.get("/state", response_model=WarehouseState)
async def state(task_id: str = "schema_drift"):
    env = get_env(task_id)
    return env.state()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
