# Activity 3-9 (Hard): End-to-End Messy Data ETL & Warehousing

## Problem Scenario
An enterprise retail chain ingests raw Point-of-Sale (POS) cash register logs into `raw_pos_transactions` and regional metadata into `store_dimension`. The POS raw logs are dirty:
1. `receipt_id` contains network duplicates that must be deduplicated.
2. `raw_store` has inconsistent casing (e.g. `'store-ca'`) and leading/trailing whitespace.
3. `raw_cashier` has irregular spaces and mixed case formatting.
4. `sale_amount` has `NULL` values from communication errors.
5. Some records reference invalid store codes that do not exist in `store_dimension`.

Build an end-to-end Python + SQL data engineering pipeline that:
1. **Pre-processes & Cleans**: Deduplicates receipts, trims and title-cases cashier names, trims and uppercases store codes.
2. **Imputes**: Imputes missing `sale_amount` with the median of valid sales.
3. **Relational Synthesis**: Performs an `INNER JOIN` with `store_dimension` (from Unit 1) to retrieve city and state tax rates.
4. **Calculates**: Computes `tax_amount = ROUND(sale_amount * tax_rate, 2)` and `total_collected = sale_amount + tax_amount`.
5. **Ingests**: Loads the clean dataset into a persistent local DuckDB analytical database table `clean_pos_sales`.

### Data Schema Overview
- **`raw_pos_transactions`**: `receipt_id` (VARCHAR), `raw_store` (VARCHAR), `raw_cashier` (VARCHAR), `sale_amount` (DECIMAL), `txn_date` (VARCHAR)
- **`store_dimension`**: `store_code` (VARCHAR), `city` (VARCHAR), `tax_rate` (DECIMAL)

### Objectives
1. Apply deduplication, string cleaning, and median imputation.
2. Join relational store dimensions.
3. Compute financial metrics.
4. Ingest into DuckDB.

## Hints
- Combine Pandas cleaning steps with DuckDB SQL queries or execute the entire pipeline inside Python before registering.
- Check row counts at each step to ensure unmapped stores or duplicates are handled according to business requirements.
