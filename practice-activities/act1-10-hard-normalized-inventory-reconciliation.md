# Activity 1-10 (Hard): Multi-Channel Inventory Reconciliation Audit

## Problem Scenario
An international logistics warehouse reconciles hardware assets by comparing inbound supplier deliveries in `purchase_receipts` against outbound customer dispatches in `sales_shipments`, grounded by an overarching master product list in `current_catalog`. 

The inventory control director requires a master stock audit report for **every single SKU** in the catalog. The report must calculate total inbound received units, total outbound shipped units, the net balance on hand (`total_received - total_shipped`), and the total net asset value (`net_balance * base_cost`). Inactive SKUs with zero movement must be preserved with a balance and valuation of 0.

### Data Schema Overview
- **`current_catalog` Table**: `sku` (VARCHAR), `sku_name` (VARCHAR), `base_cost` (DECIMAL)
- **`purchase_receipts` Table**: `receipt_id` (INT), `sku` (VARCHAR), `quantity_received` (INT)
- **`sales_shipments` Table**: `shipment_id` (INT), `sku` (VARCHAR), `quantity_shipped` (INT)

### Objectives
1. Synthesize inbound receipts and outbound shipments without producing cartesian cross-product multiplication errors.
2. Ensure SKUs with zero transactions (such as `SKU-E`) are preserved in the catalog.
3. Compute `total_received`, `total_shipped`, `net_balance`, and `inventory_valuation`.
4. Order by `inventory_valuation` descending.

## Hints
- Warning: Joining `purchase_receipts` directly to `sales_shipments` on `sku` creates a duplicate multiplication trap (fan-out) if a SKU has multiple receipts and multiple shipments!
- Pre-aggregate inbound receipts and outbound shipments by `sku` separately, or join aggregated subqueries/DataFrames back to `current_catalog`.
