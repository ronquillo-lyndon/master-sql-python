# Activity 3-2 (Easy): Logistics Freight Surcharge Fallback Imputation

## Problem Scenario
A freight management company records delivery invoice line items in `shipment_costs`. Because fuel surcharges and expedite fees are optional add-ons, carrier systems frequently transmit `NULL` values instead of zero dollars for unassessed fees. If an arithmetic addition is performed directly on columns containing `NULL`, standard relational and programmatic math evaluates the entire sum to `NULL`, resulting in missing invoice totals.

The billing department needs a report calculating the total invoice cost (`base_cost + fuel_surcharge + expedite_fee`), ensuring that missing surcharges safely default to `$0.00`.

### Data Schema Overview
- **`shipment_costs` Table**: `shipment_id` (VARCHAR), `base_cost` (DECIMAL), `fuel_surcharge` (DECIMAL), `expedite_fee` (DECIMAL)

### Objectives
1. Fallback missing `fuel_surcharge` to `0.00`.
2. Fallback missing `expedite_fee` to `0.00`.
3. Compute `total_invoice_cost`.
4. Order the output by `total_invoice_cost` descending.

## Hints
- In SQL, `COALESCE(val, fallback)` returns the first non-null argument.
- In Pandas, replace NaNs using `.fillna(0.00)` before performing column addition.
