# Activity 3-6 (Medium): Skew-Resistant Median Imputation

## Problem Scenario
Logistics delivery times in `delivery_performance` are logged as `transit_days`. Due to tracking app timeouts, several shipments contain missing (`NULL`) transit durations. Additionally, extreme customs delays created high-value outliers (e.g. 19 days) that heavily distort the arithmetic mean. 

To clean this data without introducing outlier bias, the data engineer must:
1. Detect and report the number of missing transit values.
2. Compute the **median** transit duration among non-null records (since median is robust against extreme skew).
3. Impute the computed median into all missing entries.
4. Flag rows that were imputed using a boolean indicator column `is_imputed`.

### Data Schema Overview
- **`delivery_performance` Table**: `delivery_id` (VARCHAR), `carrier` (VARCHAR), `transit_days` (DECIMAL)

### Objectives
1. Calculate statistical median on non-null numeric values.
2. Impute missing records with the calculated median.
3. Add `is_imputed` flag (`TRUE` / `FALSE` or `1` / `0`).
4. Output `delivery_id`, `carrier`, `cleaned_transit_days`, and `is_imputed`.

## Hints
- In SQL, median can be calculated using percentile functions like `PERCENTILE_CONT(0.5)` (or in DuckDB / SQLite via median window/aggregate).
- In Pandas, use `.median()` followed by `.fillna()` while creating an indicator with `.isna()`.
