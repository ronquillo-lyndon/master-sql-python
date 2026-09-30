import os
import glob
import duckdb
import pandas as pd
import numpy as np
# =============================================================
#  CONFIGURATION — change the dataset name here to switch
# =============================================================
DATASET = "dataset1-9"   # e.g. "dataset1-1", "dataset2-5", "dataset3-3"
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
#customers = tables['customers']
#orders    = tables['orders']

# merged_df = pd.merge(customers, orders, on='customer_id', how='inner')

# ordered_df = merged_df[['order_id', 
#                        'name', 
#                        'segment',
#                        'order_date',
#                        'amount']].sort_values(by='order_date', 
#                                              ascending=True)

# print(ordered_df.to_string(index=False))

customers = tables['customers']
orders = tables['orders']
products = tables['products']
order_items = tables['order_items']

report = pd.merge(
                pd.merge(
                    pd.merge(customers, 
                            orders, on='customer_id', how='left'), 
                    order_items, on='order_id', how='left'), 
                products, on='product_id', how='left')

report['quantity'] = report['quantity'].fillna(0)
report['expenditure'] = report['quantity'] * report['unit_price'].fillna(0.00)

detailed_report = report.groupby([ 'customer_id', 'name', 'tier']).agg(
                    total_quantity = ('quantity', np.sum),
                    total_expenditure = ('expenditure', np.sum)
                )
detailed_report['total_quantity'] = detailed_report['total_quantity'].fillna(0)
detailed_report['total_expenditure'] = detailed_report['total_expenditure'].fillna(0.00)

detailed_report = detailed_report.sort_values(by='total_expenditure', ascending=False)

print(detailed_report)