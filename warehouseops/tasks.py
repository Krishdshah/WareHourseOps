import pandas as pd


def task_easy():
    """Task 1: Fix a column name in a simple aggregations."""
    users = pd.DataFrame({"user_id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
    orders = pd.DataFrame({"user_id": [1, 1, 2], "amount": [100, 200, 300]})
    # The bug is 'user' instead of 'user_id'
    broken_sql = "SELECT user, SUM(amount) FROM orders GROUP BY user"
    expected = pd.DataFrame({"user_id": [1, 2], "SUM(amount)": [300, 300]})
    return {
        "tables": {"users": users, "orders": orders},
        "broken_sql": broken_sql,
        "expected": expected,
        "name": "column_fix",
    }


def task_medium():
    """Task 2: Fix an incorrect join condition causing a logic error."""
    users = pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})
    orders = pd.DataFrame({"order_id": [101, 102], "user_id": [1, 2], "amount": [100, 200]})
    # The bug is joining on u.id = o.order_id instead of u.id = o.user_id
    broken_sql = (
        "SELECT u.name, SUM(o.amount) FROM users u JOIN orders o ON u.id = o.order_id GROUP BY u.name"
    )
    expected = pd.DataFrame({"name": ["Alice", "Bob"], "SUM(o.amount)": [100, 200]})
    return {
        "tables": {"users": users, "orders": orders},
        "broken_sql": broken_sql,
        "expected": expected,
        "name": "join_fix",
    }


def task_hard():
    """Task 3: Resolve a multi-table pipeline logic error."""
    users = pd.DataFrame({"id": [1, 2]})
    orders = pd.DataFrame({"order_id": [1, 2], "user_id": [1, 2], "amount": [100, 200]})
    payments = pd.DataFrame({"order_id": [1, 2], "status": ["paid", "failed"]})
    # The bug is missing the status filter and incorrect join logic
    broken_sql = """
    SELECT user_id, SUM(amount) 
    FROM orders 
    JOIN payments ON orders.order_id = payments.order_id 
    GROUP BY user_id
    """
    # Expected result should only include 'paid' status
    expected = pd.DataFrame({"user_id": [1], "SUM(amount)": [100]})
    return {
        "tables": {"users": users, "orders": orders, "payments": payments},
        "broken_sql": broken_sql,
        "expected": expected,
        "name": "pipeline_fix",
    }


TASKS = {"easy": task_easy, "medium": task_medium, "hard": task_hard}
