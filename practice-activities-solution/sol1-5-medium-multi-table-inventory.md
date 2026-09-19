# Solution 1-5 (Medium): Multi-Table Normalized Inventory Synthesis

## SQL Implementation
```sql
SELECT 
    c.category_name,
    -- Reason: Count unique product entities defined in this category
    COUNT(DISTINCT p.product_id) AS product_count,
    -- Reason: Sum stocked quantities, falling back to 0 if all warehouse records are NULL
    COALESCE(SUM(ws.quantity_on_hand), 0) AS total_units_stocked,
    -- Reason: Multiply unit price by stocked quantity; COALESCE handles unstocked products
    COALESCE(SUM(ws.quantity_on_hand * p.unit_price), 0.00) AS total_inventory_valuation
FROM categories c
-- Reason: LEFT JOIN to ensure categories with no products or stocks are preserved
LEFT JOIN products p 
    ON c.category_id = p.category_id
-- Reason: LEFT JOIN to preserve products that currently have 0 warehouse inventory
LEFT JOIN warehouse_stocks ws 
    ON p.product_id = ws.product_id
GROUP BY c.category_name
ORDER BY total_inventory_valuation DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

categories = pd.DataFrame({
    'category_id': [1, 2, 3],
    'category_name': ['Electronics', 'Apparel', 'Office Supplies']
})

products = pd.DataFrame({
    'product_id': [10, 11, 12, 13, 14, 15],
    'category_id': [1, 1, 2, 2, 3, 3],
    'product_name': ['Noise-Cancelling Headphones', 'Ergonomic Mechanical Keyboard', 'Merino Wool Jacket', 'Trail Running Shoes', 'Heavy-Duty Paper Shredder', 'Standing Desk Converter'],
    'unit_price': [199.99, 129.50, 180.00, 110.00, 85.00, 210.00]
})

warehouse_stocks = pd.DataFrame({
    'stock_id': [1, 2, 3, 4, 5, 6],
    'product_id': [10, 10, 11, 12, 14, 15],
    'warehouse_code': ['WH-EAST', 'WH-WEST', 'WH-EAST', 'WH-CENTRAL', 'WH-WEST', 'WH-EAST'],
    'quantity_on_hand': [45, 30, 60, 15, 80, 25]
})

# Reason: Step 1 - Merge categories with products preserving all categories
cat_prod = pd.merge(categories, products, on='category_id', how='left')

# Reason: Step 2 - Merge with warehouse stocks preserving unstocked products
full_inventory = pd.merge(cat_prod, warehouse_stocks, on='product_id', how='left')

# Reason: Fill missing quantities with 0 for unstocked items
full_inventory['quantity_on_hand'] = full_inventory['quantity_on_hand'].fillna(0)

# Reason: Compute row-level extended valuation using vectorized multiplication
full_inventory['extended_value'] = full_inventory['quantity_on_hand'] * full_inventory['unit_price']

# Reason: Group by category and compute summary metrics
summary_df = full_inventory.groupby('category_name').agg(
    product_count=('product_id', 'nunique'),
    total_units_stocked=('quantity_on_hand', np.sum),
    total_inventory_valuation=('extended_value', np.sum)
).reset_index()

summary_df = summary_df.sort_values(by='total_inventory_valuation', ascending=False)
print(summary_df)
```
