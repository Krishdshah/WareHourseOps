from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

class WarehouseAction(BaseModel):
    action_type: str = Field(..., description="Action to perform: run_sql, inspect_schema, inspect_lineage, fix_query, mark_resolved")
    query: Optional[str] = Field(None, description="SQL query for run_sql or fix_query actions")
    table: Optional[str] = Field(None, description="Table name for inspect_schema action")
    metric: Optional[str] = Field(None, description="Metric name for inspect_lineage action")

class WarehouseObservation(BaseModel):
    broken_dashboard: str
    query: str
    tables: List[str]
    schema_preview: Dict[str, List[str]]
    error_logs: List[str]
    lineage_graph: Optional[Dict[str, List[str]]] = None
    available_actions: List[str]
    last_action_output: Optional[Union[str, List[Dict[str, Any]]]] = None

class WarehouseReward(BaseModel):
    reward: float
    done: bool
    info: Dict[str, Any] = {}

class WarehouseState(BaseModel):
    task_id: str
    tables: List[str]
    schemas: Dict[str, Dict[str, str]]
    dashboards: Dict[str, str]
    expected_sql: str
    resolved: bool = False
    step_count: int = 0
    max_steps: int = 15
    last_error: Optional[str] = None
    history: List[str] = []
