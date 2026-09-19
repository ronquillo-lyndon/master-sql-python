# Activity 1-1 (Easy): Inner Join Sales Matching

## Problem Scenario
A B2B enterprise software platform maintains customer accounts in a `customers` table and individual purchase records in an `orders` table. The operations team needs a clean transaction report showing every order alongside its customer details (customer name and market segment). Records from unverified customer accounts or orders with missing or orphaned customer IDs must be excluded from this report to guarantee analytical integrity.

### Data Schema Overview
- **`customers` Table**: `customer_id` (INT), `name` (VARCHAR), `segment` (VARCHAR)
- **`orders` Table**: `order_id` (INT), `customer_id` (INT), `order_date` (DATE), `amount` (DECIMAL)

### Objectives
1. Perform a set-intersection match between `orders` and `customers` based on matching `customer_id`.
2. Output `order_id`, `name`, `segment`, `order_date`, and `amount`.
3. Sort the resulting report by `order_date` in ascending order.

## Hints
- Recall that an intersection operation between two tables retains only rows with existing matching keys on both sides, effectively suppressing orphans.
- In SQL, specify the matching join condition explicitly in an `ON` clause to pair the relational attributes.
- In Pandas, the merge function defaults to or can explicitly set its join behavior to keep only shared keys between left and right DataFrames.
