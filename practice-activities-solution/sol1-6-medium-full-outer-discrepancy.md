# Solution 1-6 (Medium): Discrepancy Audit with Full Outer Join

## SQL Implementation
```sql
SELECT 
    -- Reason: Coalesce tracking numbers so we always have a non-null key regardless of which side matched
    COALESCE(l.tracking_number, p.tracking_number) AS tracking_number,
    l.erp_cost,
    p.billed_amount,
    -- Reason: Classify audit status based on existence of keys in respective tables
    CASE 
        WHEN l.tracking_number IS NOT NULL AND p.tracking_number IS NOT NULL THEN 'Matched'
        WHEN l.tracking_number IS NOT NULL AND p.tracking_number IS NULL THEN 'Missing in Platform'
        ELSE 'Missing in Legacy'
    END AS audit_status
FROM legacy_shipments l
-- Reason: FULL OUTER JOIN returns all rows from both tables ($A \cup B$)
FULL OUTER JOIN platform_receipts p 
    ON l.tracking_number = p.tracking_number
ORDER BY tracking_number ASC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

legacy_shipments = pd.DataFrame({
    'tracking_number': ['TRK-1001', 'TRK-1002', 'TRK-1003', 'TRK-1004', 'TRK-1005'],
    'erp_cost': [45.50, 120.00, 85.20, 33.10, 210.00],
    'shipper_name': ['FedEx', 'UPS', 'DHL', 'USPS', 'FreightOne']
})

platform_receipts = pd.DataFrame({
    'tracking_number': ['TRK-1001', 'TRK-1002', 'TRK-1003', 'TRK-1006', 'TRK-1007'],
    'billed_amount': [45.50, 125.00, 85.20, 74.00, 150.00],
    'carrier_status': ['Delivered', 'Delivered', 'In Transit', 'Delivered', 'Exception']
})

# Reason: how='outer' executes a full outer join aligning matching tracking numbers
merged_df = pd.merge(
    legacy_shipments, 
    platform_receipts, 
    on='tracking_number', 
    how='outer', 
    suffixes=('_legacy', '_platform')
)

# Reason: Define vectorized conditions to classify discrepancies
conditions = [
    merged_df['erp_cost'].notna() & merged_df['billed_amount'].notna(),
    merged_df['erp_cost'].notna() & merged_df['billed_amount'].isna(),
    merged_df['erp_cost'].isna() & merged_df['billed_amount'].notna()
]
choices = ['Matched', 'Missing in Platform', 'Missing in Legacy']

merged_df['audit_status'] = np.select(conditions, choices, default='Unknown')

result_df = merged_df[['tracking_number', 'erp_cost', 'billed_amount', 'audit_status']].sort_values(by='tracking_number', ascending=True)
print(result_df)
```
