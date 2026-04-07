# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Data models for the Warehouseops Environment.

The warehouseops environment is a simple test environment that echoes back messages.
"""

from openenv.core.env_server.types import Action, Observation
from pydantic import Field
from typing import Optional, Dict, Any, List


class WarehouseopsAction(Action):
    """Action for SQL Debugging."""

    action: str = Field(..., description="Action type: 'run_sql', 'edit_sql', or 'submit'")
    sql: Optional[str] = Field(None, description="The SQL query to execute or save")


class WarehouseopsObservation(Observation):
    """Observation for SQL Debugging."""

    message: str = Field(default="", description="Status message")
    schema_info: Optional[Dict[str, List[str]]] = Field(
        None, alias="schema", description="Database schema: {table_name: [columns]}"
    )
    preview: Optional[List[Dict[str, Any]]] = Field(
        None, description="First few rows of the query result"
    )
    error: Optional[str] = Field(None, description="SQL error message if execution fails")
    current_sql: Optional[str] = Field(
        None, description="The SQL currently stored in the environment"
    )

    class Config:
        populate_by_name = True
