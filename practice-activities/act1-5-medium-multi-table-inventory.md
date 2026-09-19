# Activity 1-5 (Medium): Multi-Table Normalized Inventory Synthesis

## Problem Scenario
An omnichannel retailer maintains inventory records across three normalized tables: `categories`, `products`, and `warehouse_stocks`. The supply chain analyst must synthesize these tables to produce a comprehensive valuation report showing each category name, the count of distinct products stocked, the total quantity on hand across all warehouses, and the total inventory valuation (`quantity_on_hand * unit_price`). Products with no current stock in any warehouse should still appear with a quantity of 0 and valuation of 0.00.

### Data Schema Overview
- **`categories` Table**: `category_id` (INT), `category_name` (VARCHAR)
- **`products` Table**: `product_id` (INT), `category_id` (INT), `product_name` (VARCHAR), `unit_price` (DECIMAL)
- **`warehouse_stocks` Table**: `stock_id` (INT), `product_id` (INT), `warehouse_code` (VARCHAR), `quantity_on_hand` (INT)

### Objectives
1. Join `categories` to `products`, and `products` to `warehouse_stocks`.
2. Preserve products that currently have no entries in `warehouse_stocks`.
3. Compute total units stocked and total dollar valuation per category.
4. Order results by total inventory value descending.

## Hints
- Chaining multiple joins requires careful consideration of join types; using inner joins throughout may inadvertently eliminate products or categories that have zero stock.
- The inventory valuation requires multiplying row-level quantity by unit price before aggregating, or aggregating with sum products.
- In Pandas, perform two sequential `.merge()` calls with `how='left'` starting from categories to products, then to warehouse stocks.
