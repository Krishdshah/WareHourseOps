import random
from uuid import uuid4
import duckdb
import pandas as pd

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from ..models import WarehouseopsAction, WarehouseopsObservation
from ..tasks import TASKS
from ..graders import grade_output


class WarehouseopsEnvironment(Environment):
    """
    Data Warehouse Debugger Environment.
    Agents act as data engineers to fix broken SQL queries.
    """

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        """Initialize the environment."""
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.task_data = None
        self.current_sql = ""
        self.tables = {}
        self.expected = None

    def _get_schema(self) -> dict:
        """Helper to get table schemas."""
        return {name: list(df.columns) for name, df in self.tables.items()}

    def run_sql(self, sql: str):
        """Execute SQL using DuckDB with registered dataframes."""
        try:
            con = duckdb.connect(database=":memory:")
            for name, df in self.tables.items():
                con.register(name, df)
            result = con.execute(sql).fetchdf()
            return result, None
        except Exception as e:
            return None, str(e)

    def reset(self) -> WarehouseopsObservation:
        """Reset the environment and pick a random task."""
        self._state = State(episode_id=str(uuid4()), step_count=0)
        
        # Pick a random task (easy, medium, hard)
        task_key = random.choice(list(TASKS.keys()))
        self.task_data = TASKS[task_key]()
        
        self.tables = self.task_data["tables"]
        self.current_sql = self.task_data["broken_sql"]
        self.expected = self.task_data["expected"]

        return WarehouseopsObservation(
            message=f"Task started: {self.task_data['name']}. Level: {task_key}",
            schema=self._get_schema(),
            current_sql=self.current_sql,
            done=False,
            reward=0.0,
        )

    def step(self, action: WarehouseopsAction) -> WarehouseopsObservation:  # type: ignore[override]
        """Execute an action (run_sql, edit_sql, or submit)."""
        self._state.step_count += 1
        
        act_type = action.action.lower()
        reward = 0.0
        done = False
        message = ""
        preview = None
        error = None

        if act_type == "edit_sql":
            self.current_sql = action.sql or self.current_sql
            message = "SQL updated."
            reward = 0.05  # Small reward for progress/action

        elif act_type == "run_sql":
            sql_to_run = action.sql or self.current_sql
            result, err = self.run_sql(sql_to_run)
            if err:
                error = err
                reward = -0.05  # Slight penalty for syntax error
            else:
                preview = result.head(5).to_dict("records")
                message = "Query executed successfully."
                reward = 0.1  # Reward for valid SQL execution

        elif act_type == "submit":
            result, err = self.run_sql(self.current_sql)
            if err:
                error = f"Submission failed with SQL error: {err}"
                reward = 0.0
            else:
                reward = grade_output(result, self.expected)
                message = f"Task submitted. Score: {reward}"
            done = True

        # Handle max steps (penalty for looping)
        if self._state.step_count >= 10 and not done:
            done = True
            message = "Max steps reached."
            reward -= 0.1

        return WarehouseopsObservation(
            message=message,
            schema=self._get_schema(),
            preview=preview,
            error=error,
            current_sql=self.current_sql,
            done=done,
            reward=reward,
        )

    @property
    def state(self) -> State:
        """Get the current state."""
        return self._state
