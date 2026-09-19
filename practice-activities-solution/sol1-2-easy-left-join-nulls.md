# Solution 1-2 (Easy): Preserving Inactive Accounts with Left Join

## SQL Implementation
```sql
SELECT 
    c.customer_id,
    c.company_name,
    c.region,
    -- Reason: COUNT(o.order_id) counts non-null order IDs, returning 0 for customers with no orders
    COUNT(o.order_id) AS total_orders,
    -- Reason: SUM on null values yields NULL, so COALESCE replaces NULL with 0.00
    COALESCE(SUM(o.order_value), 0.00) AS total_spend
FROM customers c
-- Reason: LEFT JOIN preserves all records from the left table (customers)
-- and populates right attributes with NULL when no order exists
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.company_name, c.region
-- Reason: Rank customers from highest to lowest spender
ORDER BY total_spend DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'company_name': ['Apex Logistics', 'Beacon Systems', 'Cascade Media', 'Dune Ventures', 'Evergreen Partners'],
    'region': ['North', 'West', 'East', 'South', 'North']
})

orders = pd.DataFrame({
    'order_id': [501, 502, 503],
    'customer_id': [1, 1, 3],
    'order_value': [450.00, 950.00, 120.00]
})

# Reason: how='left' ensures all customer rows are retained, setting missing order attributes to NaN
merged_df = pd.merge(customers, orders, on='customer_id', how='left')

# Reason: Group by customer identifiers and aggregate order metrics
# Using named aggregation with numpy for vectorized performance
report_df = merged_df.groupby(['customer_id', 'company_name', 'region']).agg(
    total_orders=('order_id', 'count'),       # count ignores NaN automatically
    total_spend=('order_value', np.sum)       # np.sum computes sum
).reset_index()

# Reason: NaN totals must be resolved to 0.00 for clean presentation
report_df['total_spend'] = report_df['total_spend'].fillna(0.00)

# Reason: Sort by total spend descending
report_df = report_df.sort_values(by='total_spend', ascending=False)

print(report_df)
```
