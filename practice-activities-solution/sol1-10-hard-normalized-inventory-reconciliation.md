# Solution 1-10 (Hard): Multi-Channel Inventory Reconciliation Audit

## SQL Implementation
```sql
-- Step 1: Pre-aggregate inbound receipts per SKU to avoid Cartesian fan-out join traps
WITH receipts_summary AS (
    SELECT sku, SUM(quantity_received) AS total_received
    FROM purchase_receipts
    GROUP BY sku
),
-- Step 2: Pre-aggregate outbound shipments per SKU
shipments_summary AS (
    SELECT sku, SUM(quantity_shipped) AS total_shipped
    FROM sales_shipments
    GROUP BY sku
)
-- Step 3: Synthesize master catalog with pre-aggregated metrics
SELECT 
    c.sku,
    c.sku_name,
    c.base_cost,
    COALESCE(r.total_received, 0) AS total_received,
    COALESCE(s.total_shipped, 0) AS total_shipped,
    -- Reason: Net balance calculation handling NULL fallbacks
    (COALESCE(r.total_received, 0) - COALESCE(s.total_shipped, 0)) AS net_balance,
    -- Reason: Asset valuation based on net on-hand units
    (COALESCE(r.total_received, 0) - COALESCE(s.total_shipped, 0)) * c.base_cost AS inventory_valuation
FROM current_catalog c
LEFT JOIN receipts_summary r ON c.sku = r.sku
LEFT JOIN shipments_summary s ON c.sku = s.sku
ORDER BY inventory_valuation DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

catalog = pd.DataFrame({
    'sku': ['SKU-A', 'SKU-B', 'SKU-C', 'SKU-D', 'SKU-E'],
    'sku_name': ['Industrial Router', 'Optical Transceiver', 'Patch Panel Cat6', 'Server Rack 42U', 'Power Distribution Unit'],
    'base_cost': [180.00, 45.00, 60.00, 650.00, 120.00]
})

purchase_receipts = pd.DataFrame({
    'receipt_id': [1, 2, 3, 4, 5],
    'sku': ['SKU-A', 'SKU-A', 'SKU-B', 'SKU-C', 'SKU-D'],
    'quantity_received': [50, 30, 200, 80, 10]
})

sales_shipments = pd.DataFrame({
    'shipment_id': [101, 102, 103, 104],
    'sku': ['SKU-A', 'SKU-B', 'SKU-C', 'SKU-D'],
    'quantity_shipped': [40, 150, 75, 8]
})

# Reason: Pre-aggregate receipts and shipments to avoid cartesian row explosion
rec_agg = purchase_receipts.groupby('sku')['quantity_received'].sum().reset_index(name='total_received')
ship_agg = sales_shipments.groupby('sku')['quantity_shipped'].sum().reset_index(name='total_shipped')

# Reason: Left merge pre-aggregated metrics to master catalog
reconciled = pd.merge(catalog, rec_agg, on='sku', how='left')
reconciled = pd.merge(reconciled, ship_agg, on='sku', how='left')

# Reason: Resolve missing movements to 0
reconciled['total_received'] = reconciled['total_received'].fillna(0).astype(int)
reconciled['total_shipped'] = reconciled['total_shipped'].fillna(0).astype(int)

# Reason: Vectorized calculation of net balance and valuation
reconciled['net_balance'] = reconciled['total_received'] - reconciled['total_shipped']
reconciled['inventory_valuation'] = reconciled['net_balance'] * reconciled['base_cost']

reconciled = reconciled.sort_values(by='inventory_valuation', ascending=False)
print(reconciled)
```
