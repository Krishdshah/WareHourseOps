from typing import Dict, Any, List

TASKS = {
    "schema_drift": {
        "id": "schema_drift",
        "name": "Task 1: Schema Drift",
        "broken_dashboard": "Daily Revenue Dashboard",
        "broken_query": "SELECT revenue FROM orders",
        "expected_sql": "SELECT total_revenue FROM orders",
        "tables": ["orders", "users"],
        "lineage": {
            "revenue": ["orders.total_revenue"]
        }
    },
    "wrong_aggregation": {
        "id": "wrong_aggregation",
        "name": "Task 2: Wrong Aggregation",
        "broken_dashboard": "Order Totals Report",
        "broken_query": "SELECT SUM(price_per_unit) FROM order_items",
        "expected_sql": "SELECT SUM(price_per_unit * quantity) FROM order_items",
        "tables": ["orders", "order_items"],
        "lineage": {
            "total_price": ["order_items.price_per_unit", "order_items.quantity"]
        }
    },
    "join_bug": {
        "id": "join_bug",
        "name": "Task 3: Multi-table Join Bug",
        "broken_dashboard": "Regional Sales Breakdown",
        # User is wrongly joined to order_items. users.id -> order_items.user_id (non-existent)
        "broken_query": "SELECT u.region, SUM(i.quantity) FROM users u JOIN order_items i ON u.id = i.user_id GROUP BY u.region",
        # Correct: users -> orders -> order_items
        "expected_sql": "SELECT u.region, SUM(i.quantity) FROM users u JOIN orders o ON u.id = o.user_id JOIN order_items i ON o.id = i.order_id GROUP BY u.region",
        "tables": ["users", "orders", "order_items"],
        "lineage": {
            "regional_quantity": ["users.region", "orders.id", "order_items.quantity"]
        }
    }
}

def grade_results(expected: List[Dict[str, Any]], actual: List[Dict[str, Any]]) -> float:
    """Deterministic grader for SQL results."""
    if not expected and not actual:
        return 1.0
    if not expected or not actual:
        return 0.0
    
    if len(expected) != len(actual):
        return 0.0
    
    match_count = 0
    total_cells = len(expected) * len(expected[0])
    
    for i in range(len(expected)):
        e_row = expected[i]
        a_row = actual[i]
        for key in e_row:
            if key in a_row and e_row[key] == a_row[key]:
                match_count += 1
                
    return match_count / total_cells if total_cells > 0 else 0.0
