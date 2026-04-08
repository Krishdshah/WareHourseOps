---
title: Warehouseops Debugger
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# WarehouseOps — Data Warehouse Debugger Environment

WarehouseOps is a professional data engineering reinforcement learning environment designed for the OpenEnv Meta Hackathon. It simulates the high-stakes task of debugging broken SQL transformation pipelines in a production data warehouse.

## 1. Environment Overview
To get started with WarehouseOps on your local machine or via Hugging Face:

- **Initial Setup**: Open the [thekrishdshah/warehouseops](https://huggingface.co/spaces/thekrishdshah/warehouseops) Space on the Hugging Face Hub.
- **Navigation**: Click the "three dots" icon in the top-right corner and select **"Run locally"**.
- **Command Execution**: Copy the provided `docker run` command to spin up the SQL debugging environment in a local container:
  ```bash
  docker run -it -p 8000:8000 thekrishdshah/warehouseops
  ```

## 2. Deploy with CLI
You can modify this environment and push your own version using the OpenEnv CLI:

- **Directory Navigation**: 
  ```bash
  cd warehouseops
  ```
- **Standard Deployment**: Deploy to your default namespace:
  ```bash
  openenv push
  ```
- **Specific Repo Deployment**: Use the `--repo-id` flag to target a specific Space:
  ```bash
  openenv push --repo-id your-username/custom-warehouseops
  ```
- **Privacy Settings**: To deploy as a private environment (visible only to you and your team):
  ```bash
  openenv push --private
  ```

## 3. Space Configuration (`openenv.yaml`)
The `openenv.yaml` manifest file in this repository controls how the Space is served. Key configuration values include:

- **name**: `warehouseops` — The unique identifier for the environment.
- **version**: `0.1.0` — The current semantic version.
- **description**: "SQL Data Warehouse Debugger Environment" — A summary of the custom SQL challenges.

## 4. Hardware Options
WarehouseOps is optimized to run on standard CPU tiers but can benefit from hardware acceleration in complex multi-agent simulations:

| Tier | vCPU | RAM | Cost |
| :--- | :--- | :--- | :--- |
| **CPU Basic (Free)** | 2 | 16GB | Free |
| **GPU T4 (Small)** | 4 | 15GB | Paid |
| **GPU L4 (Medium)** | 8 | 32GB | Paid |

---

## Tasks
1. **Easy (`column_fix`)**: Fix a column name mismatch in a `GROUP BY` clause.
2. **Medium (`join_fix`)**: Resolve a logic error in a `JOIN` condition.
3. **Hard (`pipeline_fix`)**: Multi-step pipeline fix involving joins and aggregations.

## Setup & Usage
1. **Install dependencies**:
   ```bash
   pip install pandas duckdb openenv-core pydantic
   ```
2. **Run baseline inference**:
   ```bash
   python inference.py
   ```
