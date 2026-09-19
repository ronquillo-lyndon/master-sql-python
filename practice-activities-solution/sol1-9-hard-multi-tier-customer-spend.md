# Solution 1-9 (Hard): Multi-Tier Customer Line-Item Synthesis

## SQL Implementation
```sql
SELECT 
    c.customer_id,
    c.name,
    c.tier,
    -- Reason: Count distinct orders placed by the customer
    COUNT(DISTINCT o.order_id) AS total_orders_placed,
    -- Reason: Sum total quantity of items ordered; COALESCE handles inactive clients
    COALESCE(SUM(oi.quantity), 0) AS total_units_purchased,
    -- Reason: Compute total spending across all line items
    COALESCE(SUM(oi.quantity * oi.unit_price), 0.00) AS total_expenditure
FROM customers c
-- Reason: Chain LEFT JOINs starting from the root entity (customers)
-- Using INNER JOIN here would drop inactive clients like Delta Health and Epsilon Retail
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id
LEFT JOIN order_items oi 
    ON o.order_id = oi.order_id
LEFT JOIN products p 
    ON oi.product_id = p.product_id
GROUP BY c.customer_id, c.name, c.tier
ORDER BY total_expenditure DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['Alpha Corp', 'Beta Tech', 'Gamma LLC', 'Delta Health', 'Epsilon Retail'],
    'tier': ['Gold', 'Silver', 'Bronze', 'Gold', 'Bronze']
})

orders = pd.DataFrame({
    'order_id': [5001, 5002, 5003, 5004],
    'customer_id': [1, 1, 2, 3],
    'order_date': ['2024-01-15', '2024-02-10', '2024-01-20', '2024-02-12']
})

products = pd.DataFrame({
    'product_id': [101, 102, 103, 104],
    'product_name': ['Cloud Server Blade', 'Network Switch 48P', 'SaaS Annual Seat', 'Support Ticket Pack'],
    'category': ['Infrastructure', 'Networking', 'Software', 'Services']
})

order_items = pd.DataFrame({
    'item_id': [1, 2, 3, 4, 5],
    'order_id': [5001, 5001, 5002, 5003, 5004],
    'product_id': [101, 102, 103, 104, 101],
    'quantity': [2, 1, 5, 2, 1],
    'unit_price': [1500.00, 800.00, 250.00, 400.00, 1500.00]
})

# Reason: Sequential left joins to guarantee customer retention
df_merged = pd.merge(customers, orders, on='customer_id', how='left')
df_merged = pd.merge(df_merged, order_items, on='order_id', how='left')
df_merged = pd.merge(df_merged, products, on='product_id', how='left')

# Reason: Calculate line item total value with vectorized multiplication
df_merged['line_total'] = df_merged['quantity'] * df_merged['unit_price']

# Reason: Aggregate per customer entity
customer_report = df_merged.groupby(['customer_id', 'name', 'tier']).agg(
    total_orders_placed=('order_id', 'nunique'),
    total_units_purchased=('quantity', np.sum),
    total_expenditure=('line_total', np.sum)
).reset_index()

# Reason: Resolve NaNs introduced by left-join misses
customer_report['total_units_purchased'] = customer_report['total_units_purchased'].fillna(0).astype(int)
customer_report['total_expenditure'] = customer_report['total_expenditure'].fillna(0.00)

customer_report = customer_report.sort_values(by='total_expenditure', ascending=False)
print(customer_report)
```
