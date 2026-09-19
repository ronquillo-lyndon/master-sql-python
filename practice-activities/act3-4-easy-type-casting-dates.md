# Activity 3-4 (Easy): Type Ingestion: Parsing Untyped Raw Invoices

## Problem Scenario
An ingestion pipeline loads raw vendor CSV invoices into `raw_staging_invoices`. Because CSV formats do not enforce typing, both transaction dates (`string_date`) and monetary amounts (`raw_amount_str`) were ingested as raw strings (e.g. `'2024-01-15'` and `'1450.50'`). Before downstream financial modeling or date-based partitioning can occur, the data engineer must cast these strings into native SQL `DATE` and `DECIMAL` types.

### Data Schema Overview
- **`raw_staging_invoices` Table**: `invoice_id` (VARCHAR), `string_date` (VARCHAR), `raw_amount_str` (VARCHAR)

### Objectives
1. Cast `string_date` to an authentic `DATE` type.
2. Cast `raw_amount_str` to a `DECIMAL(10, 2)` or `FLOAT` type.
3. Compute a calculated column `sales_tax` as 8% (`amount * 0.08`), rounded to two decimal places.
4. Order the output by `invoice_date` ascending.

## Hints
- In SQL, use `CAST(column AS DATE)` and `CAST(column AS DECIMAL(10, 2))`.
- In Pandas, convert dates using `pd.to_datetime()` and numeric strings using `.astype(float)`.
