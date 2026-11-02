"""
Module 11: SQL and Relational Data
CS 5045: Computation for the Data Sciences
Virginia Tech, Applied Data Science MS Program

Demonstrates the five computational operations expressed as SQL clauses against
an in-memory SQLite database, then bridges the result back into pandas.

No external file: both tables are created inline, exactly as in the assignment.

Run from the Code/ folder:
    python3 example.py
"""

import sqlite3
import pandas as pd


# =============================================================================
# REPRESENT: create the database and both tables
# =============================================================================

print("=" * 60)
print("REPRESENT: Building the relational database")
print("=" * 60)

conn = sqlite3.connect(":memory:")

conn.execute("""
    CREATE TABLE customers (
        customer_id  INTEGER PRIMARY KEY,
        name         TEXT,
        state        TEXT,
        total_spent  REAL,
        year         INTEGER
    )
""")

conn.execute("""
    CREATE TABLE orders (
        order_id     INTEGER PRIMARY KEY,
        customer_id  INTEGER REFERENCES customers,
        product      TEXT,
        amount       REAL
    )
""")

customers_data = [
    (1,  "Alice Chen",    "CA", 1250.00, 2021),
    (2,  "Bob Martin",    "TX",  480.00, 2022),
    (3,  "Carmen Lopez",  "CA",  895.50, 2020),
    (4,  "David Kim",     "NY", 2300.00, 2021),
    (5,  "Emma Walsh",    "CA",  320.00, 2023),
    (6,  "Frank Osei",    "TX", 1750.00, 2020),
    (7,  "Grace Park",    "NY",  640.00, 2022),
    (8,  "Henry Brown",   "FL",  890.00, 2021),
    (9,  "Isabel Torres", "CA", 1100.00, 2022),
    (10, "James Wilson",  "TX",  250.00, 2023),
    (11, "Karen Adams",   "NY", 3100.00, 2020),
    (12, "Luis Rivera",   "FL",  700.00, 2021),
    (13, "Maya Patel",    "CA",  550.00, 2022),
    (14, "Noah Clark",    "NY",  980.00, 2021),
    (15, "Olivia Scott",  "FL", 1400.00, 2020),
]
conn.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", customers_data)

orders_data = [
    (101, 1,  "Laptop",      999.00),
    (102, 1,  "Mouse",        45.00),
    (103, 3,  "Keyboard",     89.50),
    (104, 4,  "Monitor",     650.00),
    (105, 4,  "Webcam",      120.00),
    (106, 6,  "Headphones",  250.00),
    (107, 7,  "USB Hub",      35.00),
    (108, 8,  "Desk Lamp",    75.00),
    (109, 9,  "Tablet",      520.00),
    (110, 11, "Laptop",     1100.00),
    (111, 11, "Printer",     299.00),
    (112, 14, "Microphone",  185.00),
]
conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders_data)
conn.commit()

print("customers: 15 rows, 5 columns")
print("orders:    12 rows, 4 columns (not every customer has an order)")

# =============================================================================
# FILTER: WHERE keeps rows that meet a condition
# =============================================================================

print("\n" + "=" * 60)
print("FILTER: WHERE")
print("=" * 60)

rows = conn.execute("""
    SELECT name, state, total_spent
    FROM customers
    WHERE state = 'CA' AND total_spent > 800
""").fetchall()
print("California customers with total_spent > 800:")
for row in rows:
    print(" ", row)

# =============================================================================
# COMMUNICATE: ORDER BY + LIMIT surfaces the rows that matter
# =============================================================================

print("\n" + "=" * 60)
print("COMMUNICATE: ORDER BY + LIMIT")
print("=" * 60)

rows = conn.execute("""
    SELECT name, state, total_spent
    FROM customers
    ORDER BY total_spent DESC
    LIMIT 5
""").fetchall()
print("Top 5 customers by spending:")
for row in rows:
    print(" ", row)

# =============================================================================
# AGGREGATE: GROUP BY collapses rows into per-group summaries
# =============================================================================

print("\n" + "=" * 60)
print("AGGREGATE: GROUP BY")
print("=" * 60)

rows = conn.execute("""
    SELECT state, COUNT(*) AS num_customers
    FROM customers
    GROUP BY state
    ORDER BY num_customers DESC
""").fetchall()
print("Customers per state:")
for row in rows:
    print(" ", row)

# HAVING: Filter applied after aggregation, on the grouped result
rows = conn.execute("""
    SELECT state, COUNT(*) AS num_customers
    FROM customers
    GROUP BY state
    HAVING COUNT(*) > 3
""").fetchall()
print("\nStates with more than 3 customers (HAVING, not WHERE):")
for row in rows:
    print(" ", row)

# =============================================================================
# REPRESENT (extended): JOIN combines rows across two tables
# =============================================================================

print("\n" + "=" * 60)
print("REPRESENT + AGGREGATE: JOIN across tables")
print("=" * 60)

rows = conn.execute("""
    SELECT customers.name, SUM(orders.amount) AS order_total
    FROM customers
    INNER JOIN orders
      ON customers.customer_id = orders.customer_id
    GROUP BY customers.name
    ORDER BY order_total DESC
""").fetchall()
print("Total order amount per customer (INNER JOIN keeps only matched rows):")
for row in rows:
    print(f"  {row[0]:<16} ${row[1]:.2f}")

# LEFT JOIN preserves customers with no matching orders
no_orders = conn.execute("""
    SELECT customers.name
    FROM customers
    LEFT JOIN orders
      ON customers.customer_id = orders.customer_id
    WHERE orders.order_id IS NULL
""").fetchall()
print(f"\nCustomers with no orders ({len(no_orders)}, via LEFT JOIN):")
for row in no_orders:
    print(" ", row[0])

# =============================================================================
# COMMUNICATE: pd.read_sql_query() bridges SQL results into pandas
# =============================================================================

print("\n" + "=" * 60)
print("COMMUNICATE: pd.read_sql_query() -- SQL results as a DataFrame")
print("=" * 60)

df = pd.read_sql_query("""
    SELECT state, COUNT(*) AS num_customers
    FROM customers
    GROUP BY state
    ORDER BY num_customers DESC
""", conn)
print(df)
print("\ndtypes:")
print(df.dtypes)

conn.close()
