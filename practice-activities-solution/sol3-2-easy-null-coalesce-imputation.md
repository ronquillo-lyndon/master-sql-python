# Solution 3-2 (Easy): Logistics Freight Surcharge Fallback Imputation

## SQL Implementation
```sql
SELECT 
    shipment_id,
    base_cost,
    -- Reason: Replace NULL surcharges with 0.00 to avoid arithmetic poison where NULL + X = NULL
    COALESCE(fuel_surcharge, 0.00) AS imputed_fuel_surcharge,
    COALESCE(expedite_fee, 0.00) AS imputed_expedite_fee,
    -- Reason: Safely calculate total invoice cost using coalesced values
    base_cost + COALESCE(fuel_surcharge, 0.00) + COALESCE(expedite_fee, 0.00) AS total_invoice_cost
FROM shipment_costs
ORDER BY total_invoice_cost DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

shipment_costs = pd.DataFrame({
    'shipment_id': ['SHP-001', 'SHP-002', 'SHP-003', 'SHP-004', 'SHP-005'],
    'base_cost': [250.00, 400.00, 180.00, 520.00, 310.00],
    'fuel_surcharge': [35.00, np.nan, 20.00, np.nan, 45.00],
    'expedite_fee': [50.00, 0.00, np.nan, np.nan, 25.00]
})

# Reason: Inspect missingness volume for quality control
missing_fuel = shipment_costs['fuel_surcharge'].isna().sum()
missing_expedite = shipment_costs['expedite_fee'].isna().sum()
print(f"[QC] Found {missing_fuel} missing fuel surcharges and {missing_expedite} missing expedite fees.")

# Reason: Default optional add-on fees to 0.00
shipment_costs['fuel_surcharge'] = shipment_costs['fuel_surcharge'].fillna(0.00)
shipment_costs['expedite_fee'] = shipment_costs['expedite_fee'].fillna(0.00)

# Reason: Perform vectorized column addition to compute total invoice cost
shipment_costs['total_invoice_cost'] = (
    shipment_costs['base_cost'] + 
    shipment_costs['fuel_surcharge'] + 
    shipment_costs['expedite_fee']
)

result_df = shipment_costs.sort_values(by='total_invoice_cost', ascending=False)
print(result_df)
```
