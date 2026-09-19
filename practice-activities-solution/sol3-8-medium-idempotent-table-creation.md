# Solution 3-8 (Medium): Building Idempotent Ingestion Pipelines

## Python & DuckDB Implementation
```python
import pandas as pd
import duckdb

raw_ledger = pd.DataFrame({
    'entry_id': [1001, 1002, 1003, 1004],
    'account_code': ['ACC-ASSET-01', 'ACC-LIAB-02', 'ACC-REV-03', 'ACC-EXP-04'],
    'entry_date': ['2024-03-01', '2024-03-01', '2024-03-01', '2024-03-01'],
    'amount': [1500.00, -500.00, 2800.00, -750.00]
})

def run_idempotent_pipeline(conn, df):
    # Reason: Register the input DataFrame
    conn.register('staging_feed', df)
    
    # Reason: 1. Idempotent DDL: CREATE TABLE IF NOT EXISTS avoids table collision errors
    conn.execute("""
        CREATE TABLE IF NOT EXISTS persistent_ledger (
            entry_id INT PRIMARY KEY,
            account_code VARCHAR(20),
            entry_date DATE,
            amount DECIMAL(10, 2)
        );
    """)
    
    # Reason: 2. Idempotent Ingestion: To avoid duplicate rows on re-runs,
    # delete overlapping partition dates before inserting fresh batch
    conn.execute("""
        DELETE FROM persistent_ledger 
        WHERE entry_date IN (SELECT DISTINCT CAST(entry_date AS DATE) FROM staging_feed);
    """)
    
    conn.execute("""
        INSERT INTO persistent_ledger
        SELECT entry_id, account_code, CAST(entry_date AS DATE), amount
        FROM staging_feed;
    """)
    
    count = conn.execute("SELECT COUNT(*) FROM persistent_ledger;").fetchone()[0]
    return count

conn = duckdb.connect(':memory:')

# Run 1
count_run_1 = run_idempotent_pipeline(conn, raw_ledger)
print(f"Run 1 completed. Total rows in persistent_ledger: {count_run_1}")

# Run 2 (Simulating pipeline retry)
count_run_2 = run_idempotent_pipeline(conn, raw_ledger)
print(f"Run 2 completed. Total rows in persistent_ledger: {count_run_2}")

assert count_run_1 == count_run_2 == len(raw_ledger), "Idempotency failed: Row count drifted!"
print("Idempotency verified: Pipeline executed multiple times with identical final state.")
conn.close()
```

## SQL Script Equivalent
```sql
-- Step 1: Safe table creation
CREATE TABLE IF NOT EXISTS persistent_ledger (
    entry_id INT PRIMARY KEY,
    account_code VARCHAR(20),
    entry_date DATE,
    amount DECIMAL(10, 2)
);

-- Step 2: Clear staging partition to avoid duplicate accumulation
DELETE FROM persistent_ledger 
WHERE entry_date = '2024-03-01';

-- Step 3: Insert verified data
INSERT INTO persistent_ledger (entry_id, account_code, entry_date, amount)
SELECT entry_id, account_code, CAST(entry_date AS DATE), amount
FROM staging_feed;
```
