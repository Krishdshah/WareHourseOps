import sqlite3
import os
from typing import List, Dict, Any

class DataManager:
    def __init__(self, db_path: str = "warehouse.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initializes the database with schema and seed data."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Users Table
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                region TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Orders Table
        # Task 1 (Easy) will rename 'total_revenue' to 'revenue' or vice versa.
        # We start with 'total_revenue' to simulate "drift" if the query expects 'revenue'.
        cursor.execute("""
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                status TEXT,
                total_revenue REAL, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Order Items Table
        cursor.execute("""
            CREATE TABLE order_items (
                id INTEGER PRIMARY KEY,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price_per_unit REAL,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        """)

        # Payments Table
        cursor.execute("""
            CREATE TABLE payments (
                id INTEGER PRIMARY KEY,
                order_id INTEGER,
                amount REAL,
                payment_method TEXT,
                status TEXT,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        """)

        # Seed Data
        users = [
            (1, 'Alice', 'alice@example.com', 'North America'),
            (2, 'Bob', 'bob@example.com', 'Europe'),
            (3, 'Charlie', 'charlie@example.com', 'Asia')
        ]
        cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?)", 
                          [(u[0], u[1], u[2], u[3], '2023-01-01 10:00:00') for u in users])

        orders = [
            (101, 1, 'completed', 150.0, '2023-05-01 12:00:00'),
            (102, 2, 'completed', 80.0, '2023-05-02 14:00:00'),
            (103, 1, 'pending', 45.0, '2023-05-03 09:00:00')
        ]
        cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders)

        order_items = [
            (1, 101, 501, 2, 75.0),
            (2, 101, 502, 1, 0.0), # price integrated in total_revenue
            (3, 102, 503, 1, 80.0),
            (4, 103, 501, 1, 45.0)
        ]
        cursor.executemany("INSERT INTO order_items VALUES (?,?,?,?,?)", order_items)

        conn.commit()
        conn.close()

    def run_query(self, query: str) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_schema(self, table_name: str) -> List[tuple]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema = cursor.fetchall()
        conn.close()
        return schema
