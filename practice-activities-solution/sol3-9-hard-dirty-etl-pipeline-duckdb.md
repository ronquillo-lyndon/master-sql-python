# Solution 3-9 (Hard): End-to-End Messy Data ETL & Warehousing

## Python & DuckDB Production ETL Pipeline
```python
import pandas as pd
import numpy as np
import duckdb

raw_pos_transactions = pd.DataFrame({
    'receipt_id': ['RCP-001', 'RCP-001', 'RCP-002', 'RCP-003', 'RCP-004', 'RCP-005'],
    'raw_store': [' STORE-NY ', ' STORE-NY ', 'store-ca', 'STORE-TX', ' STORE-NY', 'STORE-UNKNOWN'],
    'raw_cashier': ['  JOHN DOE  ', '  JOHN DOE  ', 'alice smith', 'bob johnson', 'John Doe ', 'charlie'],
    'sale_amount': [150.00, 150.00, np.nan, 320.50, 95.00, 210.00],
    'txn_date': ['2024-02-01', '2024-02-01', '2024-02-01', '2024-02-02', '2024-02-02', '2024-02-03']
})

store_dimension = pd.DataFrame({
    'store_code': ['STORE-NY', 'STORE-CA', 'STORE-TX'],
    'city': ['New York', 'San Francisco', 'Austin'],
    'tax_rate': [0.088, 0.095, 0.082]
})

def run_pos_etl(db_path=":memory:"):
    df = raw_pos_transactions.copy()
    
    # Reason: 1. Deduplication - drop duplicate receipt IDs
    df = df.drop_duplicates(subset=['receipt_id'], keep='first').copy()
    
    # Reason: 2. String Standardization - clean store codes and cashier names
    df['store_code'] = df['raw_store'].apply(lambda x: str(x).strip().upper())
    df['cashier_name'] = df['raw_cashier'].apply(lambda x: str(x).strip().title())
    df['txn_date'] = pd.to_datetime(df['txn_date'])
    
    # Reason: 3. Median Imputation for missing numerical sales
    median_sale = df['sale_amount'].median()
    df['sale_amount'] = df['sale_amount'].fillna(median_sale)
    
    # Reason: 4. Relational Synthesis (Unit 1 Inner Join with store dimension)
    enriched_df = pd.merge(df, store_dimension, on='store_code', how='inner')
    
    # Reason: 5. Financial derived calculations
    enriched_df['tax_amount'] = (enriched_df['sale_amount'] * enriched_df['tax_rate']).round(2)
    enriched_df['total_collected'] = enriched_df['sale_amount'] + enriched_df['tax_amount']
    
    final_df = enriched_df[[
        'receipt_id', 'store_code', 'city', 'cashier_name', 
        'txn_date', 'sale_amount', 'tax_amount', 'total_collected'
    ]]
    
    # Reason: 6. DuckDB Ingestion
    conn = duckdb.connect(db_path)
    conn.register('virtual_clean_pos', final_df)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clean_pos_sales AS 
        SELECT * FROM virtual_clean_pos;
    """)
    
    warehouse_output = conn.execute("SELECT * FROM clean_pos_sales;").fetchdf()
    conn.close()
    return warehouse_output

result = run_pos_etl()
print("Final Ingested POS Sales in Warehouse:")
print(result)
```

## SQL Direct Imputation and Join Equivalent
```sql
WITH deduplicated_pos AS (
    SELECT 
        receipt_id,
        TRIM(UPPER(raw_store)) AS store_code,
        TRIM(raw_cashier) AS cashier_name,
        sale_amount,
        CAST(txn_date AS DATE) AS txn_date,
        ROW_NUMBER() OVER (PARTITION BY receipt_id ORDER BY txn_date ASC) AS rn
    FROM raw_pos_transactions
),
clean_pos AS (
    SELECT 
        receipt_id,
        store_code,
        cashier_name,
        COALESCE(sale_amount, 150.00) AS sale_amount,
        txn_date
    FROM deduplicated_pos
    WHERE rn = 1
)
SELECT 
    p.receipt_id,
    p.store_code,
    s.city,
    p.cashier_name,
    p.txn_date,
    p.sale_amount,
    ROUND(p.sale_amount * s.tax_rate, 2) AS tax_amount,
    p.sale_amount + ROUND(p.sale_amount * s.tax_rate, 2) AS total_collected
FROM clean_pos p
INNER JOIN store_dimension s ON p.store_code = s.store_code
ORDER BY p.txn_date ASC;
```
