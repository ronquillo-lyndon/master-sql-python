# Solution 3-7 (Medium): Zero-Copy DuckDB Virtual View Ingestion

## Python & DuckDB Implementation
```python
import pandas as pd
import duckdb

supplier_catalog = pd.DataFrame({
    'sku': ['SUP-101', 'SUP-102', 'SUP-103', 'SUP-104', 'SUP-105'],
    'brand': ['LogiPro', 'LogiPro', 'AnkerPower', 'AnkerPower', 'KeySonic'],
    'wholesale_price': [45.00, 85.50, 25.00, 65.00, 110.00],
    'available_stock': [250, 140, 500, 180, 95]
})

# Reason: 1. Initialize an in-process DuckDB analytical session
conn = duckdb.connect(database=':memory:')

# Reason: 2. Register Pandas DataFrame as an in-engine virtual view (zero-copy query interface)
conn.register('virtual_supplier_catalog', supplier_catalog)

# Reason: 3. Execute analytical SQL to aggregate and ingest into a physical DuckDB table
conn.execute("""
    CREATE TABLE brand_valuation_summary AS
    SELECT 
        brand,
        COUNT(sku) AS total_skus,
        ROUND(AVG(wholesale_price), 2) AS avg_wholesale_price,
        SUM(wholesale_price * available_stock) AS total_brand_valuation
    FROM virtual_supplier_catalog
    GROUP BY brand
    ORDER BY total_brand_valuation DESC;
""")

# Reason: 4. Validate table creation by fetching results back into Pandas
result_df = conn.execute("SELECT * FROM brand_valuation_summary;").fetchdf()

print("Ingested DuckDB Table Results:")
print(result_df)

conn.close()
```

## SQL Equivalent Query Inside DuckDB
```sql
-- Query executed inside DuckDB virtual view
CREATE TABLE brand_valuation_summary AS
SELECT 
    brand,
    COUNT(sku) AS total_skus,
    ROUND(AVG(wholesale_price), 2) AS avg_wholesale_price,
    SUM(wholesale_price * available_stock) AS total_brand_valuation
FROM virtual_supplier_catalog
GROUP BY brand
ORDER BY total_brand_valuation DESC;
```
