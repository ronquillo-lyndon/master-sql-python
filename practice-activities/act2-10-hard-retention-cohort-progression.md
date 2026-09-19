# Activity 2-10 (Hard): Customer Retention & Purchase Interval Pipeline

## Problem Scenario
A subscription e-commerce merchant wants to analyze customer repurchase habits by connecting user registration channels in `customer_signups` with transaction histories in `customer_purchases`. 

Building on concepts from Unit 1 (Relational Joins) and Unit 2 (CTEs and Window Functions), construct an analytical query that:
1. Performs a `LEFT JOIN` from `customer_signups` to `customer_purchases` to preserve registered users who made 0 purchases.
2. For purchasing customers, assigns a sequential order number (`order_seq`) using `ROW_NUMBER()`.
3. Computes the interval in days between the current purchase and the immediate prior purchase (`days_since_prior_purchase`) using `LAG()`. For a customer's first purchase, display `0`.
4. Formats customers with zero purchases to show `order_seq = 0` and `days_since_prior_purchase = 0`.

### Data Schema Overview
- **`customer_signups` Table**: `customer_id` (INT), `signup_date` (DATE), `channel` (VARCHAR)
- **`customer_purchases` Table**: `purchase_id` (INT), `customer_id` (INT), `purchase_date` (DATE), `amount` (DECIMAL)

### Objectives
1. Synthesize `customer_signups` and `customer_purchases`.
2. Compute `order_seq` partitioned by customer and ordered by purchase date.
3. Compute date delta in days from prior purchase.
4. Preserve non-purchasing users.
5. Order output by `customer_id` ascending, then `purchase_date` ascending.

## Hints
- Combine a `LEFT JOIN` with CTEs and window functions.
- In SQL, calculate day differences between dates using date subtraction or `DATEDIFF` depending on the dialect. In SQLite/DuckDB, date subtraction `CAST(purchase_date AS DATE) - CAST(prior_date AS DATE)` yields day intervals.
- In Pandas, subtract datetime Series and extract the `.dt.days` attribute.
