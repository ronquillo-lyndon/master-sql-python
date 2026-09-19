"""
Validation test suite to run solutions against DuckDB and Pandas
to ensure syntax validity, logical correctness, and clean execution.
"""

import duckdb
import pandas as pd
import numpy as np
import sympy as sp
import os

print("--- Running Test Validations ---")

# Test 1: Unit 1 SQL & Python (Act 1-10 Normalized Inventory Reconciliation)
conn = duckdb.connect(':memory:')
with open("practice-activities-sql/dataset1-10-hard-normalized-inventory-reconciliation.sql") as f:
    conn.execute(f.read())

sql_1_10 = """
WITH receipts_summary AS (
    SELECT sku, SUM(quantity_received) AS total_received
    FROM purchase_receipts
    GROUP BY sku
),
shipments_summary AS (
    SELECT sku, SUM(quantity_shipped) AS total_shipped
    FROM sales_shipments
    GROUP BY sku
)
SELECT 
    c.sku,
    c.sku_name,
    c.base_cost,
    COALESCE(r.total_received, 0) AS total_received,
    COALESCE(s.total_shipped, 0) AS total_shipped,
    (COALESCE(r.total_received, 0) - COALESCE(s.total_shipped, 0)) AS net_balance,
    (COALESCE(r.total_received, 0) - COALESCE(s.total_shipped, 0)) * c.base_cost AS inventory_valuation
FROM current_catalog c
LEFT JOIN receipts_summary r ON c.sku = r.sku
LEFT JOIN shipments_summary s ON c.sku = s.sku
ORDER BY inventory_valuation DESC;
"""
res_1_10 = conn.execute(sql_1_10).fetchdf()
assert len(res_1_10) == 5, f"Expected 5 SKUs, got {len(res_1_10)}"
print("[PASS] Act 1-10 SQL executed successfully")
conn.close()

# Test 2: Unit 2 SQL & Python (Act 2-9 SymPy & Moving Average)
p0, p1, p2 = sp.symbols('p0 p1 p2')
w0, w1, w2 = sp.symbols('w0 w1 w2')
formula = (p0 * w0 + p1 * w1 + p2 * w2) / (w0 + w1 + w2)
vf = formula.subs({w0: 0.5, w1: 0.3, w2: 0.2})
assert str(vf) == "0.5*p0 + 0.3*p1 + 0.2*p2"
print("[PASS] Act 2-9 SymPy verified successfully")

# Test 3: Unit 3 End-to-End Pipeline (Act 3-9)
conn = duckdb.connect(':memory:')
with open("practice-activities-sql/dataset3-9-hard-dirty-etl-pipeline-duckdb.sql") as f:
    conn.execute(f.read())

clean_pos_sql = """
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
"""
res_3_9 = conn.execute(clean_pos_sql).fetchdf()
assert len(res_3_9) == 4, f"Expected 4 matched valid rows, got {len(res_3_9)}"
print("[PASS] Act 3-9 SQL ETL verified successfully")
conn.close()

# Test 4: Unit 3 Statistical Anomaly Split (Act 3-10)
conn = duckdb.connect(':memory:')
with open("practice-activities-sql/dataset3-10-hard-anomaly-audit-ingestion.sql") as f:
    conn.execute(f.read())

act_3_10_sql = """
WITH windowed_telemetry AS (
    SELECT 
        reading_id,
        device_id,
        reading_timestamp,
        COALESCE(pressure_psi, MEDIAN(pressure_psi) OVER (PARTITION BY device_id)) AS pressure_psi,
        ROUND(AVG(pressure_psi) OVER (
            PARTITION BY device_id 
            ORDER BY reading_timestamp ASC 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 2) AS rolling_avg_psi
    FROM iot_factory_readings
),
anomaly_flagged AS (
    SELECT 
        *,
        ROUND(ABS(pressure_psi - rolling_avg_psi) / rolling_avg_psi, 3) AS anomaly_score,
        CASE 
            WHEN (ABS(pressure_psi - rolling_avg_psi) / rolling_avg_psi) > 0.50 THEN TRUE 
            ELSE FALSE 
        END AS is_anomaly
    FROM windowed_telemetry
)
SELECT 
    COUNT(*) FILTER (WHERE is_anomaly = FALSE) AS clean_count,
    COUNT(*) FILTER (WHERE is_anomaly = TRUE) AS anomaly_count
FROM anomaly_flagged;
"""
res_3_10 = conn.execute(act_3_10_sql).fetchall()
clean_cnt, anomaly_cnt = res_3_10[0]
assert anomaly_cnt >= 1, "Expected at least 1 anomaly"
print(f"[PASS] Act 3-10 Anomaly Split verified: {clean_cnt} clean, {anomaly_cnt} anomalies")
conn.close()

print("\n--- ALL VERIFICATIONS PASSED SUCCESSFULLY ---")
