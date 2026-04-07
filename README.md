# WarehouseOps: SQL Data Warehouse Debugger Environment

**WarehouseOps** is a high-fidelity reinforcement learning environment designed for the [OpenEnv PyTorch Meta Hackathon](https://openenv.ai). It simulates real-world data engineering workflows where an AI agent acts as a Data Engineer responsible for debugging and fixing broken SQL transformation pipelines.

## 🌟 Key Features
- **Real-World Utility**: Simulates professional data engineering tasks (debugging dashboards, fixing joins, resolving aggregation errors).
- **DuckDB Powered**: High-performance, in-memory SQL execution for fast agent training and evaluation.
- **Deterministic Grading**: Programmatic evaluation comparing agent output DataFrames against expected ground truth.
- **Partial Rewards**: Dense reward signals for syntax correctness, column matching, and row-count heuristics.
- **OpenEnv Compliant**: Fully supports the `step()`, `reset()`, and `state()` API with strictly typed Pydantic models.

## 🛠️ Environment Tasks
The environment includes a suite of three deterministic tasks ranging in difficulty:
1. **Easy (`column_fix`)**: Fix a simple column naming mismatch that breaks a `GROUP BY` clause.
2. **Medium (`join_fix`)**: Resolve a logic error in a table join condition causing incorrect row counts.
3. **Hard (`pipeline_fix`)**: A multi-step debugging task involving filtering, joining, and complex window-like aggregations.

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or 3.11 (Recommended)
- Docker Desktop (for local verification)
- [OpenEnv Core](https://github.com/meta-pytorch/OpenEnv)

### Installation
1. Clone the repository and navigate to the project root.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r warehouseops/server/requirements.txt
   ```

### Running Local Validation
To ensure the environment is correctly structured and compliant:
```bash
cd warehouseops
openenv validate
```

### Running the Baseline Agent
The project includes a baseline inference script using the OpenAI API:
```bash
# Set your API keys
export OPENAI_API_KEY="your-key"
export HF_TOKEN="your-hf-token"

# Run the inference baseline
python warehouseops/inference.py
```

## 📦 Deployment
The environment is structured as a **Space** and can be deployed directly to Hugging Face:
1. Login to Hugging Face:
   ```bash
   hf auth login
   ```
2. Push the environment:
   ```bash
   openenv push --repo-id your-username/warehouseops
   ```

## 📂 Project Structure
- `warehouseops/`: Core environment package.
  - `server/`: FastAPI server and environment logic.
  - `models.py`: Pydantic Action/Observation models.
  - `tasks.py`: Definitions of debugging challenges.
  - `graders.py`: Grading and reward logic.
  - `inference.py`: Baseline benchmarking script.
- `README.md`: This file.

## ⚖️ License
This project is licensed under the BSD-style license - see the [LICENSE](LICENSE) file for details.
