# Solution 1-1 (Easy): Inner Join Sales Matching

## SQL Implementation
```sql
-- Select relevant order attributes and customer demographic fields
SELECT 
    o.order_id,
    c.name,
    c.segment,
    o.order_date,
    o.amount
FROM orders o
-- Reason: INNER JOIN returns records only where customer_id exists in both tables ($A \cap B$).
-- This filters out orphaned orders (e.g., customer_id 99) and customers without transactions.
INNER JOIN customers c 
    ON o.customer_id = c.customer_id
-- Reason: Ensure chronological presentation of sales events
ORDER BY o.order_date ASC;
```

## Python Implementation
```python
import pandas as pd

# Load mock tables as DataFrames
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['Alice Corp', 'Bob Labs', 'Charlie Retail', 'Delta Inc', 'Echo Solutions'],
    'segment': ['Enterprise', 'SMB', 'Retail', 'SMB', 'Enterprise']
})

orders = pd.DataFrame({
    'order_id': [101, 102, 103, 104, 105, 106],
    'customer_id': [1, 1, 2, 3, 3, 99],
    'order_date': ['2024-01-10', '2024-01-15', '2024-01-16', '2024-01-20', '2024-01-22', '2024-01-25'],
    'amount': [1250.00, 850.50, 320.00, 150.00, 90.00, 500.00]
})

# Reason: pd.merge with how='inner' executes set intersection on 'customer_id'
# Orphan customer_id 99 is discarded because it has no corresponding match in customers
merged_df = pd.merge(orders, customers, on='customer_id', how='inner')

# Reason: Reorder columns and sort chronologically as required
result_df = merged_df[['order_id', 'name', 'segment', 'order_date', 'amount']].sort_values(by='order_date', ascending=True)

print(result_df)
```
