# Activity 1-9 (Hard): Multi-Tier Customer Line-Item Synthesis

## Problem Scenario
An enterprise B2B SaaS platform stores client accounts in `customers`, order headers in `orders`, itemized line details in `order_items`, and product classifications in `products`. The executive analytics committee wants a comprehensive report detailing total sales expenditure per customer and customer tier across individual product categories. 

Crucially, **all** registered customers must be preserved in the report. If a customer has never placed an order, or has not purchased products within a category, their spending must be reported as `$0.00`, and their total ordered units as `0`.

### Data Schema Overview
- **`customers` Table**: `customer_id` (INT), `name` (VARCHAR), `tier` (VARCHAR)
- **`orders` Table**: `order_id` (INT), `customer_id` (INT), `order_date` (DATE)
- **`order_items` Table**: `item_id` (INT), `order_id` (INT), `product_id` (INT), `quantity` (INT), `unit_price` (DECIMAL)
- **`products` Table**: `product_id` (INT), `product_name` (VARCHAR), `category` (VARCHAR)

### Objectives
1. Connect `customers` -> `orders` -> `order_items` -> `products`.
2. Ensure every customer is preserved via appropriate `LEFT JOIN` operations.
3. Compute `total_quantity` and `total_expenditure` (`SUM(quantity * unit_price)`).
4. Group by customer attributes (`customer_id`, `name`, `tier`).
5. Replace NULLs with 0.00 and sort by `total_expenditure` descending.

## Hints
- Chaining multiple `LEFT JOIN` statements preserves the root left entity throughout the entire pipeline.
- Be careful: if an intermediate table like `orders` or `order_items` is joined with an `INNER JOIN`, any inactive customers from the first table will be silently eliminated.
- In Pandas, perform sequential left merges, multiply quantity by unit price, fill NaNs, and aggregate with `.groupby()`.
