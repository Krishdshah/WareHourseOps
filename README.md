# WarehouseOps: Analytics Debugging Environment

WarehouseOps is a real-world analytics debugging RL environment for OpenEnv. It simulates the daily workflow of a data engineer responsible for fixing broken SQL dashboards in a data warehouse.

## Overview

In this environment, an agent acts as a data engineer. A "broken dashboard" is provided with a faulty SQL query. The agent must inspect schemas, analyze data lineage, run exploratory queries, and fix the SQL logic to match the expected output.

### Features
- **SQLite Backend**: Uses a real SQL execution engine for deterministic grading.
- **Dense Rewards**: Provides feedback for schema inspection, partial SQL fixes, and correct outputs.
- **3 Task Difficulties**:
  - **Easy (Schema Drift)**: Fix a query where a column name has changed.
  - **Medium (Wrong Aggregation)**: Fix a metric calculation requiring a JOIN and a multi-column formula.
  - **Hard (Join Bug)**: Detect and fix a missing intermediate join in a multi-table query.

## Action Space

The agent interacts via a structured action space:
- `run_sql(query)`: Execute a query against the warehouse.
- `inspect_schema(table)`: View the column definitions for a table.
- `inspect_lineage(metric)`: Trace the upstream columns for a specific dashboard metric.
- `fix_query(query)`: Update the dashboard with a fixed SQL query.
- `mark_resolved()`: Submit the fix for final grading.

## Observation Space

The agent receives:
- `broken_dashboard`: Name of the failing report.
- `query`: The current (broken) SQL.
- `tables`: List of available tables.
- `schema_preview`: Sample columns for all tables.
- `error_logs`: Recent execution errors.
- `lineage_graph`: Relationships between metrics and source columns.

## Setup & Usage

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the OpenEnv server:
   ```bash
   python app.py
   ```

### Docker

Build and run the container:
```bash
docker build -t warehouse-ops .
docker run -p 8000:8000 warehouse-ops
```

### Inference

Run the baseline script (requires `OPENAI_API_KEY`):
```bash
python inference.py
```

## Reward Function

| Action | Reward |
| :--- | :--- |
| Inspect Schema | +0.02 |
| Inspect Lineage | +0.05 |
| Partial SQL Fix | +0.20 |
| Correct Output | +1.00 |
| Invalid SQL | -0.10 |
| Looping/Repetition | -0.05 |

## OpenEnv Compliance

Metadata is defined in `openenv.yaml`. The environment implements the standard `reset()`, `step()`, and `state()` endpoints.
