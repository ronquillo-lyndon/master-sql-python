# Activity 2-8 (Medium): Multi-Step Funnel with Common Table Expressions (CTEs)

## Problem Scenario
Store transactions are recorded at high frequency in `store_orders`. The regional director wants to identify the single top-performing store for each business day based on total daily revenue. Solve this challenge cleanly using Common Table Expressions (CTEs) to organize the query into a logical pipeline:
1. **Step 1 (Daily Aggregation CTE)**: Sum the order value per `store_id` and `order_date`.
2. **Step 2 (Ranking CTE)**: Assign a daily performance rank (`ROW_NUMBER`) to stores within each date based on total revenue descending.
3. **Step 3 (Final Output)**: Filter the pipeline to extract only the `#1` ranked store for each day.

### Data Schema Overview
- **`store_orders` Table**: `order_id` (INT), `store_id` (INT), `order_timestamp` (TIMESTAMP), `order_value` (DECIMAL)

### Objectives
1. Implement CTEs with `WITH ... AS (...)`.
2. Cast timestamps to date grain for grouping.
3. Filter ranked rows where `rank = 1`.
4. Order the output chronologically by date.

## Hints
- CTEs make complex queries readable by turning nested subqueries into sequential modular steps.
- In Pandas, CTE pipelines correspond directly to sequential intermediate named DataFrames.
