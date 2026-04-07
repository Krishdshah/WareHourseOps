import asyncio
import os
import json
from typing import List, Optional
from openai import OpenAI
from models import WarehouseopsAction
from server.warehouseops_environment import WarehouseopsEnvironment

# Load environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", HF_TOKEN)

MAX_STEPS = 5


def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done, error):
    # Action might contain newlines, so we escape them for logs
    safe_action = str(action).replace("\n", "\\n")
    print(
        f"[STEP] step={step} action={safe_action} reward={reward} done={done} error={error}",
        flush=True,
    )


def log_end(success, steps, score, rewards):
    print(
        f"[END] success={success} steps={steps} score={score} rewards={rewards}",
        flush=True,
    )


def get_client():
    return OpenAI(api_key=OPENAI_API_KEY, base_url=API_BASE_URL)


def get_model_action(obs) -> WarehouseopsAction:
    """Standardize the LLM call to return a WarehouseopsAction."""
    client = get_client()
    prompt = f"""
You are a SQL Data Engineer debugging a broken pipeline.
Current Task Message: {obs.message}
Current SQL: {obs.current_sql}
Schema: {obs.schema_info}
Last Error (if any): {obs.error}
Last Preview (if any): {obs.preview}

Available Actions:
1. run_sql: Test a SQL query.
2. edit_sql: Update the stored SQL query.
3. submit: Submit the current SQL for final grading.

Respond ONLY with a JSON object in this format:
{{"action": "run_sql" | "edit_sql" | "submit", "sql": "YOUR_SQL_HERE"}}
"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content)
        return WarehouseopsAction(action=data["action"], sql=data.get("sql"))
    except Exception as e:
        # Fallback to a no-op or default submit if LLM fails
        return WarehouseopsAction(action="submit")


async def run_task(task_level: str):
    env = WarehouseopsEnvironment()
    # We force the env to use a specific task for deterministic benchmarking if needed,
    # but here we follow the standard reset() which picks random.
    # To be exactly reproducible, we'd wrap this.
    
    obs = env.reset()
    rewards = []
    steps_taken = 0
    success = False
    
    log_start(task=task_level, env="warehouseops", model=MODEL_NAME)
    
    try:
        for step in range(1, MAX_STEPS + 1):
            action = get_model_action(obs)
            obs = env.step(action)
            
            reward = obs.reward
            done = obs.done
            
            rewards.append(reward)
            steps_taken = step
            
            log_step(step=step, action=f"{action.action}: {action.sql}", reward=reward, done=done, error=obs.error)
            
            if done:
                break
        
        total_reward = sum(rewards)
        # Score is normalized 0-1. Max possible is roughly 1.0 (from submit) + small step rewards.
        score = min(max(total_reward, 0.0), 1.0)
        success = score >= 0.8
        
    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    # In a real benchmark, we'd loop over easy, medium, hard
    asyncio.run(run_task("baseline_test"))
