import sqlite3
from typing import Dict, Any, List, Optional
from models import WarehouseAction, WarehouseObservation, WarehouseReward, WarehouseState
from data_manager import DataManager
from tasks import TASKS, grade_results

class WarehouseEnv:
    def __init__(self, task_id: str = "schema_drift"):
        self.data_manager = DataManager()
        self.task_id = task_id
        self._init_state()

    def _init_state(self):
        task = TASKS[self.task_id]
        self._state = WarehouseState(
            task_id=self.task_id,
            tables=task["tables"],
            schemas=self._get_all_schemas(task["tables"]),
            dashboards={task["broken_dashboard"]: task["broken_query"]},
            expected_sql=task["expected_sql"],
            resolved=False,
            step_count=0,
            history=[]
        )

    def _get_all_schemas(self, tables: List[str]) -> Dict[str, Dict[str, str]]:
        schemas = {}
        for table in tables:
            rows = self.data_manager.get_schema(table)
            schemas[table] = {row[1]: row[2] for row in rows} # name: type
        return schemas

    async def reset(self) -> WarehouseObservation:
        self._init_state()
        return self._get_observation()

    def _get_observation(self, last_output: Any = None) -> WarehouseObservation:
        task = TASKS[self.task_id]
        schema_preview = {}
        for table in self._state.tables:
            schema_preview[table] = list(self._state.schemas[table].keys())

        return WarehouseObservation(
            broken_dashboard=task["broken_dashboard"],
            query=self._state.dashboards[task["broken_dashboard"]],
            tables=self._state.tables,
            schema_preview=schema_preview,
            error_logs=[self._state.last_error] if self._state.last_error else [],
            lineage_graph=task["lineage"],
            available_actions=["run_sql", "inspect_schema", "inspect_lineage", "fix_query", "mark_resolved"],
            last_action_output=last_output
        )

    async def step(self, action: WarehouseAction) -> WarehouseReward:
        self._state.step_count += 1
        reward = 0.0
        info = {"action": action.action_type}
        last_output = None

        try:
            if action.action_type == "run_sql":
                if not action.query:
                    raise ValueError("SQL query is required for run_sql action.")
                # We also check if the query uses non-existent columns (hallucination check)
                last_output = self.data_manager.run_query(action.query)
                reward += 0.02 # Small reward for exploring
            
            elif action.action_type == "inspect_schema":
                if not action.table or action.table not in self._state.tables:
                    raise ValueError(f"Table '{action.table}' not found.")
                last_output = str(self._state.schemas[action.table])
                reward += 0.02

            elif action.action_type == "inspect_lineage":
                task = TASKS[self.task_id]
                if not action.metric or action.metric not in task["lineage"]:
                    raise ValueError(f"Metric '{action.metric}' not found in lineage.")
                last_output = str(task["lineage"][action.metric])
                reward += 0.05

            elif action.action_type == "fix_query":
                if not action.query:
                    raise ValueError("Fixed query cannot be empty.")
                task = TASKS[self.task_id]
                self._state.dashboards[task["broken_dashboard"]] = action.query
                
                # Intermediate reward calculation
                # Check for correct column/aggregation
                if self.task_id == "schema_drift" and "total_revenue" in action.query:
                    reward += 0.2
                if self.task_id == "wrong_aggregation" and "*" in action.query and "quantity" in action.query:
                    reward += 0.2
                if self.task_id == "join_bug" and "orders" in action.query.lower():
                    reward += 0.2

                last_output = "Query updated successfully."

            elif action.action_type == "mark_resolved":
                # Final evaluation
                task = TASKS[self.task_id]
                current_query = self._state.dashboards[task["broken_dashboard"]]
                
                try:
                    actual_results = self.data_manager.run_query(current_query)
                    expected_results = self.data_manager.run_query(self._state.expected_sql)
                    
                    score = grade_results(expected_results, actual_results)
                    reward += score * 1.0 # Max reward is 1.0
                    
                    if score >= 0.99:
                        self._state.resolved = True
                    last_output = f"Grader Score: {score}"
                except Exception as e:
                    reward -= 0.05 # Penalty for grading a broken query
                    last_output = f"Invalid SQL in dashboard: {str(e)}"
            
            else:
                raise ValueError(f"Unknown action type: {action.action_type}")

        except Exception as e:
            reward -= 0.1 # Penalty for error
            self._state.last_error = str(e)
            last_output = f"Error: {str(e)}"

        # Looping penalty
        action_str = f"{action.action_type}:{action.query or action.table or action.metric}"
        if action_str in self._state.history:
            reward -= 0.05
        self._state.history.append(action_str)

        # Max steps
        done = self._state.resolved or self._state.step_count >= self._state.max_steps
        
        return WarehouseReward(
            reward=reward,
            done=done,
            info={"msg": last_output}
        )

    def state(self) -> WarehouseState:
        return self._state
