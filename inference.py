import os
import asyncio
import textwrap
from typing import List, Optional, Dict, Any
from openai import OpenAI
from models import WarehouseAction, WarehouseObservation, WarehouseReward

# Environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
HF_TOKEN = os.getenv("HF_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# OpenEnv Server URL
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:8000")

SYSTEM_PROMPT = textwrap.dedent(
    """
    You are a Data Engineering Agent debugging a broken data warehouse.
    You have actions: run_sql(query), inspect_schema(table), inspect_lineage(metric), fix_query(query), mark_resolved().
    
    Your goal is to fix the broken dashboard query by identifying schema drift, wrong aggregations, or join bugs.
    
    Always start by inspecting the relevant schemas and lineage.
    When you are confident, use fix_query to update the SQL.
    Finally, use mark_resolved() to submit and get the final score.
    
    Respond in JSON format: {"action_type": "...", "query": "...", "table": "...", "metric": "..."}
    """
).strip()

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error or 'null'}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)

async def main():
    import httpx
    client = OpenAI(api_key=OPENAI_API_KEY or HF_TOKEN, base_url=API_BASE_URL)
    
    # Task list to run
    tasks = ["schema_drift", "wrong_aggregation", "join_bug"]
    
    for task_id in tasks:
        log_start(task=task_id, env="warehouse_ops", model=MODEL_NAME)
        
        rewards = []
        steps_taken = 0
        success = False
        final_score = 0.0
        
        async with httpx.AsyncClient() as http_client:
            # Reset
            resp = await http_client.post(f"{ENV_BASE_URL}/reset", json={"task_id": task_id})
            obs = WarehouseObservation(**resp.json())
            
            history = []
            
            for step in range(1, 16):
                # Get model action
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Observation: {obs.model_dump_json()}\nHistory: {history[-3:]}"}
                ]
                
                try:
                    completion = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages,
                        response_format={"type": "json_object"}
                    )
                    action_data = completion.choices[0].message.content
                    # Parse and call step
                    resp = await http_client.post(f"{ENV_BASE_URL}/step", json={"task_id": task_id, "action": action_data})
                    result = WarehouseReward(**resp.json())
                    
                    rewards.append(result.reward)
                    steps_taken = step
                    
                    log_step(step=step, action=action_data.strip(), reward=result.reward, done=result.done, error=None)
                    
                    if result.done:
                        final_score = result.reward # Assuming last reward is the grader score if resolved
                        success = final_score >= 0.9
                        break
                        
                    # Update observation for next step (simplified - normally get from state)
                    state_resp = await http_client.get(f"{ENV_BASE_URL}/state", params={"task_id": task_id})
                    obs_resp = await http_client.post(f"{ENV_BASE_URL}/reset", json={"task_id": task_id}) # Mocking next obs
                    obs = WarehouseObservation(**obs_resp.json()) 
                    obs.error_logs = [result.info.get("msg")] if result.info.get("msg") else []
                    
                except Exception as e:
                    log_step(step=step, action="error", reward=-1.0, done=True, error=str(e))
                    break
            
            log_end(success=success, steps=steps_taken, score=final_score, rewards=rewards)

if __name__ == "__main__":
    asyncio.run(main())
