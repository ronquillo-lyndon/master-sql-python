# Activity 1-8 (Medium): Payment Channel Breakdown & Settlement

## Problem Scenario
A fintech settlement engine logs all digital payment attempts in a `transactions` table. The risk and accounting department requires a summary per `payment_method`. For each payment channel, compute the total number of transactions attempted, the count of unique paying customers, the total settlement volume (sum of amounts for 'Completed' transactions only), and the count of refunded transactions.

### Data Schema Overview
- **`transactions` Table**: `txn_id` (VARCHAR), `customer_id` (INT), `payment_method` (VARCHAR), `amount` (DECIMAL), `status` (VARCHAR)

### Objectives
1. Group records by `payment_method`.
2. Compute `total_attempts` (COUNT), `unique_customers` (COUNT DISTINCT).
3. Compute `completed_volume` (sum amount where `status = 'Completed'`).
4. Compute `refunded_count` (count where `status = 'Refunded'`).
5. Order by `completed_volume` descending.

## Hints
- Conditional aggregation combines `SUM` or `COUNT` with a `CASE WHEN` statement inside the aggregation function.
- In Pandas, you can create helper indicator/filtered columns before grouping or use lambda aggregations with boolean masks.
