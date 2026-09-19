# Activity 1-4 (Easy): Filtering Aggregated Store Sales

## Problem Scenario
A retail chain records individual daily sales transactions in a `store_sales` table. Executive leadership wants to reward regional divisions that have proven strong quarterly revenue. Specifically, the team must identify only those regions where the total cumulative sales amount across all stores in the region strictly exceeds $3,000.00, along with the count of distinct active stores in that qualifying region.

### Data Schema Overview
- **`store_sales` Table**: `sale_id` (INT), `store_id` (INT), `region` (VARCHAR), `sale_amount` (DECIMAL), `sale_date` (DATE)

### Objectives
1. Group sales by `region`.
2. Compute `total_sales` (SUM) and `active_store_count` (COUNT DISTINCT).
3. Filter out regions whose `total_sales` is less than or equal to $3,000.00.
4. Order the qualifying regions by `total_sales` in descending order.

## Hints
- Remember that a `WHERE` clause filters rows before aggregation occurs, whereas a `HAVING` clause filters summary metrics after grouping.
- In Pandas, this translates to performing a `.groupby().agg()` first, and then applying boolean filtering on the resulting aggregate column.
