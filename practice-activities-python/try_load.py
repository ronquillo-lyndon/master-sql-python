import os
import glob
import duckdb
import pandas as pd

# =============================================================
#  CONFIGURATION — change the dataset name here to switch
# =============================================================
DATASET = "dataset1-1"   # e.g. "dataset1-1", "dataset2-5", "dataset3-3"
# =============================================================

# Resolve path to the .sql file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_DIR  = os.path.join(BASE_DIR, "practice-activities-sql")

matches = sorted(glob.glob(os.path.join(SQL_DIR, f"{DATASET}*.sql")))
if not matches:
    raise FileNotFoundError(
        f"No dataset found matching '{DATASET}' in:\n  {SQL_DIR}\n"
        f"Check the folder for available datasets."
    )

sql_file = matches[0]
print(f"[+] Loading: {os.path.basename(sql_file)}")

# Load the SQL into an in-memory DuckDB connection
conn = duckdb.connect()
with open(sql_file, "r", encoding="utf-8") as f:
    conn.execute(f.read())

# Fetch all table names from the loaded dataset
table_names = [row[0] for row in conn.execute("SHOW TABLES").fetchall()]
print(f"[+] Tables loaded: {table_names}\n")

# Convert every table to a pandas DataFrame automatically
tables = {}
for name in table_names:
    tables[name] = conn.execute(f"SELECT * FROM {name}").df()
    print(f"--- {name} ({len(tables[name])} rows) ---")
    print(tables[name].to_string(index=False))
    print()

# Make each table available as its own variable for easy access
# e.g. if tables are 'customers' and 'orders', you get:
#   customers = tables['customers']
#   orders    = tables['orders']
for name, df in tables.items():
    globals()[name] = df

conn.close()

# =============================================================
#  PRACTICE SANDBOX — write your pandas code below
#  All tables from the dataset are ready as DataFrames
# =============================================================

# --- Example using dataset1-1 (customers + orders) ---
# Feel free to modify, delete, or replace this with your own code
customers = tables['customers']
orders    = tables['orders']
merged_df = pd.merge(customers, orders, on='customer_id', how='inner')
report_df = merged_df.sort_values(by="order_date", ascending=True)

print("=== Merged & Sorted Report ===")
print(report_df.to_string(index=False))
