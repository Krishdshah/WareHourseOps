# WarehouseOps — Data Warehouse Debugger Environment

A real-world RL environment for training and evaluating data engineering agents.

## Overview
Agents act as Data Engineers tasked with debugging and fixing broken SQL pipelines in a data warehouse. They must inspect schemas, run test queries, and submit verified SQL fixes.

## Tasks
1. **Easy (`column_fix`)**: Fix a column name mismatch in a `GROUP BY` clause.
2. **Medium (`join_fix`)**: Resolve a logic error in a `JOIN` condition between two tables.
3. **Hard (`pipeline_fix`)**: Multi-step pipeline fix involving joins, aggregations, and row filtering.

## Interface
- **Action space**: 
  - `run_sql`: Execute a query and see results.
  - `edit_sql`: Update the current draft SQL.
  - `submit`: Final submission for grading.
- **Observation space**:
  - `schema`: Table names and column lists.
  - `preview`: First 5 rows of query results.
  - `error`: Traceback if SQL execution fails.
  - `current_sql`: The current state of the code.

## Reward Function
- **+1.0**: Exact match with expected output.
- **+0.1 to +0.9**: Partial rewards for correct columns, row counts, and value heuristics.
- **-0.05**: Small penalty for syntax errors.
- **-0.1**: Penalty for reaching max steps without a fix.

## Setup & Usage
1. Install dependencies:
   ```bash
   pip install pandas duckdb openenv-core pydantic
   ```
2. Run baseline inference:
   ```bash
   python inference.py
   ```
3. Build for deployment:
   ```bash
   openenv build
   ```

## Requirements
- Python 3.10+
- Docker
