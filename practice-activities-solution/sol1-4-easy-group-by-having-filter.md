# Solution 1-4 (Easy): Filtering Aggregated Store Sales

## SQL Implementation
```sql
SELECT 
    region,
    -- Reason: Count unique store identifiers participating in the region
    COUNT(DISTINCT store_id) AS active_store_count,
    -- Reason: Sum total gross sales generated across the region
    SUM(sale_amount) AS total_sales
FROM store_sales
GROUP BY region
-- Reason: HAVING filters aggregated group metrics; WHERE cannot filter on SUM()
HAVING SUM(sale_amount) > 3000.00
ORDER BY total_sales DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

store_sales = pd.DataFrame({
    'sale_id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'store_id': [101, 101, 102, 201, 201, 301, 301, 401, 402],
    'region': ['North', 'North', 'North', 'South', 'South', 'East', 'East', 'West', 'West'],
    'sale_amount': [1500.00, 2300.00, 1100.00, 600.00, 450.00, 3200.00, 2800.00, 750.00, 800.00],
    'sale_date': ['2024-02-01', '2024-02-02', '2024-02-01', '2024-02-01', '2024-02-03', '2024-02-01', '2024-02-04', '2024-02-02', '2024-02-03']
})

# Reason: Group by region and calculate unique store count and total sales
region_agg = store_sales.groupby('region').agg(
    active_store_count=('store_id', 'nunique'),
    total_sales=('sale_amount', np.sum)
).reset_index()

# Reason: Replicate SQL HAVING clause by filtering the aggregated DataFrame
qualifying_regions = region_agg[region_agg['total_sales'] > 3000.00]

# Reason: Sort results by total_sales descending
result_df = qualifying_regions.sort_values(by='total_sales', ascending=False)

print(result_df)
```
