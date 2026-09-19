# Activity 1-2 (Easy): Preserving Inactive Accounts with Left Join

## Problem Scenario
A logistics company tracks accounts in a `customers` table and booked freight shipments in an `orders` table. Account managers need an executive overview of all registered clients, their total spend, and their shipment count. Inactive clients who have not yet booked any shipments must remain visible in the report with a spend and shipment count of 0.00 rather than missing rows or unhandled NULLs.

### Data Schema Overview
- **`customers` Table**: `customer_id` (INT), `company_name` (VARCHAR), `region` (VARCHAR)
- **`orders` Table**: `order_id` (INT), `customer_id` (INT), `order_value` (DECIMAL)

### Objectives
1. Preserve every customer record regardless of whether matching orders exist.
2. Calculate total order value and total order count per customer.
3. Fallback missing values to `0.00` (or `0`).
4. Sort by total order value in descending order.

## Hints
- A left join preserves all records from the primary entity table on the left, filling unmatched right-side attributes with NULL.
- When computing summaries over optional relationships, aggregations over NULL right-side keys produce NULL or 0 depending on the function.
- Remember to use a fallback function in SQL and a filling method in Pandas to ensure empty metrics become zero.
