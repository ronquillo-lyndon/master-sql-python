"""
Script to generate all 30 Activity markdown files and all 30 Solution markdown files
for Units 1, 2, and 3 adhering strictly to practice-activities-guide.md.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACT_DIR = os.path.join(BASE_DIR, "practice-activities")
SOL_DIR = os.path.join(BASE_DIR, "practice-activities-solution")

os.makedirs(ACT_DIR, exist_ok=True)
os.makedirs(SOL_DIR, exist_ok=True)

def write_act(filename, content):
    filepath = os.path.join(ACT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def write_sol(filename, content):
    filepath = os.path.join(SOL_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print("Generating Unit 1 Activities and Solutions...")

# ==========================================
# UNIT 1
# ==========================================

# 1-1 Easy: Inner Join Sales
write_act("act1-1-easy-inner-join-sales.md", """# Activity 1-1 (Easy): Inner Join Sales Matching

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
""")

write_sol("sol1-1-easy-inner-join-sales.md", """# Solution 1-1 (Easy): Inner Join Sales Matching

## SQL Implementation
```sql
-- Select relevant order attributes and customer demographic fields
SELECT 
    o.order_id,
    c.name,
    c.segment,
    o.order_date,
    o.amount
FROM orders o
-- Reason: INNER JOIN returns records only where customer_id exists in both tables ($A \\cap B$).
-- This filters out orphaned orders (e.g., customer_id 99) and customers without transactions.
INNER JOIN customers c 
    ON o.customer_id = c.customer_id
-- Reason: Ensure chronological presentation of sales events
ORDER BY o.order_date ASC;
```

## Python Implementation
```python
import pandas as pd

# Load mock tables as DataFrames
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['Alice Corp', 'Bob Labs', 'Charlie Retail', 'Delta Inc', 'Echo Solutions'],
    'segment': ['Enterprise', 'SMB', 'Retail', 'SMB', 'Enterprise']
})

orders = pd.DataFrame({
    'order_id': [101, 102, 103, 104, 105, 106],
    'customer_id': [1, 1, 2, 3, 3, 99],
    'order_date': ['2024-01-10', '2024-01-15', '2024-01-16', '2024-01-20', '2024-01-22', '2024-01-25'],
    'amount': [1250.00, 850.50, 320.00, 150.00, 90.00, 500.00]
})

# Reason: pd.merge with how='inner' executes set intersection on 'customer_id'
# Orphan customer_id 99 is discarded because it has no corresponding match in customers
merged_df = pd.merge(orders, customers, on='customer_id', how='inner')

# Reason: Reorder columns and sort chronologically as required
result_df = merged_df[['order_id', 'name', 'segment', 'order_date', 'amount']].sort_values(by='order_date', ascending=True)

print(result_df)
```
""")

# 1-2 Easy: Left Join Nulls
write_act("act1-2-easy-left-join-nulls.md", """# Activity 1-2 (Easy): Preserving Inactive Accounts with Left Join

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
""")

write_sol("sol1-2-easy-left-join-nulls.md", """# Solution 1-2 (Easy): Preserving Inactive Accounts with Left Join

## SQL Implementation
```sql
SELECT 
    c.customer_id,
    c.company_name,
    c.region,
    -- Reason: COUNT(o.order_id) counts non-null order IDs, returning 0 for customers with no orders
    COUNT(o.order_id) AS total_orders,
    -- Reason: SUM on null values yields NULL, so COALESCE replaces NULL with 0.00
    COALESCE(SUM(o.order_value), 0.00) AS total_spend
FROM customers c
-- Reason: LEFT JOIN preserves all records from the left table (customers)
-- and populates right attributes with NULL when no order exists
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.company_name, c.region
-- Reason: Rank customers from highest to lowest spender
ORDER BY total_spend DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'company_name': ['Apex Logistics', 'Beacon Systems', 'Cascade Media', 'Dune Ventures', 'Evergreen Partners'],
    'region': ['North', 'West', 'East', 'South', 'North']
})

orders = pd.DataFrame({
    'order_id': [501, 502, 503],
    'customer_id': [1, 1, 3],
    'order_value': [450.00, 950.00, 120.00]
})

# Reason: how='left' ensures all customer rows are retained, setting missing order attributes to NaN
merged_df = pd.merge(customers, orders, on='customer_id', how='left')

# Reason: Group by customer identifiers and aggregate order metrics
# Using named aggregation with numpy for vectorized performance
report_df = merged_df.groupby(['customer_id', 'company_name', 'region']).agg(
    total_orders=('order_id', 'count'),       # count ignores NaN automatically
    total_spend=('order_value', np.sum)       # np.sum computes sum
).reset_index()

# Reason: NaN totals must be resolved to 0.00 for clean presentation
report_df['total_spend'] = report_df['total_spend'].fillna(0.00)

# Reason: Sort by total spend descending
report_df = report_df.sort_values(by='total_spend', ascending=False)

print(report_df)
```
""")

# 1-3 Easy: Basic Aggregations
write_act("act1-3-easy-basic-aggregations.md", """# Activity 1-3 (Easy): Departmental Salary Benchmarks

## Problem Scenario
Human Resources wants to audit the internal compensation structure across organizational departments recorded in the `employees` table. To establish baseline compensation bands, leadership needs a summary per department displaying the total headcount, the minimum salary, the maximum salary, and the average salary rounded to two decimal places.

### Data Schema Overview
- **`employees` Table**: `emp_id` (INT), `emp_name` (VARCHAR), `dept_name` (VARCHAR), `salary` (DECIMAL)

### Objectives
1. Group employees by `dept_name`.
2. Compute `headcount` (COUNT), `min_salary` (MIN), `max_salary` (MAX), and `avg_salary` (AVG rounded to 2 decimals).
3. Order the report alphabetically by department name.

## Hints
- Aggregation functions collapse multiple employee rows into a single departmental metric row.
- Non-aggregated columns selected in the query must be specified in the grouping expression.
- In Pandas, consider using `.agg()` with dictionary or named tuples alongside NumPy vectorized functions (`np.mean`, `np.min`, `np.max`).
""")

write_sol("sol1-3-easy-basic-aggregations.md", """# Solution 1-3 (Easy): Departmental Salary Benchmarks

## SQL Implementation
```sql
SELECT 
    dept_name,
    -- Reason: Count total employee records per department group
    COUNT(emp_id) AS headcount,
    -- Reason: Compute the lowest compensation boundary in the department
    MIN(salary) AS min_salary,
    -- Reason: Compute the highest compensation boundary in the department
    MAX(salary) AS max_salary,
    -- Reason: Compute arithmetic mean salary and round to 2 decimal places
    ROUND(AVG(salary), 2) AS avg_salary
FROM employees
-- Reason: Collapse row-level employee data into department groups
GROUP BY dept_name
ORDER BY dept_name ASC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'emp_name': ['Sarah Chen', 'Dave Miller', 'Elena Rostova', 'Marcus Brody', 'Chloe Price', 'Tom Alvarez', 'Priya Patel', 'Liam Vance'],
    'dept_name': ['Engineering', 'Engineering', 'Engineering', 'Marketing', 'Marketing', 'Sales', 'Sales', 'Sales'],
    'salary': [125000.00, 140000.00, 110000.00, 85000.00, 92000.00, 78000.00, 105000.00, 96000.00]
})

# Reason: Replicate SQL GROUP BY using .groupby() and vectorized NumPy aggregations
dept_summary = employees.groupby('dept_name').agg(
    headcount=('emp_id', 'count'),
    min_salary=('salary', np.min),
    max_salary=('salary', np.max),
    avg_salary=('salary', np.mean)
).reset_index()

# Reason: Round avg_salary to 2 decimal places and sort alphabetically
dept_summary['avg_salary'] = dept_summary['avg_salary'].round(2)
dept_summary = dept_summary.sort_values(by='dept_name', ascending=True)

print(dept_summary)
```
""")

# 1-4 Easy: Group By Having Filter
write_act("act1-4-easy-group-by-having-filter.md", """# Activity 1-4 (Easy): Filtering Aggregated Store Sales

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
""")

write_sol("sol1-4-easy-group-by-having-filter.md", """# Solution 1-4 (Easy): Filtering Aggregated Store Sales

## SQL Implementation
```sql
SELECT 
    region,
    -- Reason: Count unique store identifiers participating in the region
    COUNT(DISTINCT store_id) AS active_store_count,
    -- Reason: Sum total gross sales generated across the region
    SUM(sale_amount) AS total_sales
FROM store_sales
GROUP BY region
-- Reason: HAVING filters aggregated group metrics; WHERE cannot filter on SUM()
HAVING SUM(sale_amount) > 3000.00
ORDER BY total_sales DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

store_sales = pd.DataFrame({
    'sale_id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'store_id': [101, 101, 102, 201, 201, 301, 301, 401, 402],
    'region': ['North', 'North', 'North', 'South', 'South', 'East', 'East', 'West', 'West'],
    'sale_amount': [1500.00, 2300.00, 1100.00, 600.00, 450.00, 3200.00, 2800.00, 750.00, 800.00],
    'sale_date': ['2024-02-01', '2024-02-02', '2024-02-01', '2024-02-01', '2024-02-03', '2024-02-01', '2024-02-04', '2024-02-02', '2024-02-03']
})

# Reason: Group by region and calculate unique store count and total sales
region_agg = store_sales.groupby('region').agg(
    active_store_count=('store_id', 'nunique'),
    total_sales=('sale_amount', np.sum)
).reset_index()

# Reason: Replicate SQL HAVING clause by filtering the aggregated DataFrame
qualifying_regions = region_agg[region_agg['total_sales'] > 3000.00]

# Reason: Sort results by total_sales descending
result_df = qualifying_regions.sort_values(by='total_sales', ascending=False)

print(result_df)
```
""")

# 1-5 Medium: Multi Table Inventory
write_act("act1-5-medium-multi-table-inventory.md", """# Activity 1-5 (Medium): Multi-Table Normalized Inventory Synthesis

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
""")

write_sol("sol1-5-medium-multi-table-inventory.md", """# Solution 1-5 (Medium): Multi-Table Normalized Inventory Synthesis

## SQL Implementation
```sql
SELECT 
    c.category_name,
    -- Reason: Count unique product entities defined in this category
    COUNT(DISTINCT p.product_id) AS product_count,
    -- Reason: Sum stocked quantities, falling back to 0 if all warehouse records are NULL
    COALESCE(SUM(ws.quantity_on_hand), 0) AS total_units_stocked,
    -- Reason: Multiply unit price by stocked quantity; COALESCE handles unstocked products
    COALESCE(SUM(ws.quantity_on_hand * p.unit_price), 0.00) AS total_inventory_valuation
FROM categories c
-- Reason: LEFT JOIN to ensure categories with no products or stocks are preserved
LEFT JOIN products p 
    ON c.category_id = p.category_id
-- Reason: LEFT JOIN to preserve products that currently have 0 warehouse inventory
LEFT JOIN warehouse_stocks ws 
    ON p.product_id = ws.product_id
GROUP BY c.category_name
ORDER BY total_inventory_valuation DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

categories = pd.DataFrame({
    'category_id': [1, 2, 3],
    'category_name': ['Electronics', 'Apparel', 'Office Supplies']
})

products = pd.DataFrame({
    'product_id': [10, 11, 12, 13, 14, 15],
    'category_id': [1, 1, 2, 2, 3, 3],
    'product_name': ['Noise-Cancelling Headphones', 'Ergonomic Mechanical Keyboard', 'Merino Wool Jacket', 'Trail Running Shoes', 'Heavy-Duty Paper Shredder', 'Standing Desk Converter'],
    'unit_price': [199.99, 129.50, 180.00, 110.00, 85.00, 210.00]
})

warehouse_stocks = pd.DataFrame({
    'stock_id': [1, 2, 3, 4, 5, 6],
    'product_id': [10, 10, 11, 12, 14, 15],
    'warehouse_code': ['WH-EAST', 'WH-WEST', 'WH-EAST', 'WH-CENTRAL', 'WH-WEST', 'WH-EAST'],
    'quantity_on_hand': [45, 30, 60, 15, 80, 25]
})

# Reason: Step 1 - Merge categories with products preserving all categories
cat_prod = pd.merge(categories, products, on='category_id', how='left')

# Reason: Step 2 - Merge with warehouse stocks preserving unstocked products
full_inventory = pd.merge(cat_prod, warehouse_stocks, on='product_id', how='left')

# Reason: Fill missing quantities with 0 for unstocked items
full_inventory['quantity_on_hand'] = full_inventory['quantity_on_hand'].fillna(0)

# Reason: Compute row-level extended valuation using vectorized multiplication
full_inventory['extended_value'] = full_inventory['quantity_on_hand'] * full_inventory['unit_price']

# Reason: Group by category and compute summary metrics
summary_df = full_inventory.groupby('category_name').agg(
    product_count=('product_id', 'nunique'),
    total_units_stocked=('quantity_on_hand', np.sum),
    total_inventory_valuation=('extended_value', np.sum)
).reset_index()

summary_df = summary_df.sort_values(by='total_inventory_valuation', ascending=False)
print(summary_df)
```
""")

# 1-6 Medium: Full Outer Discrepancy
write_act("act1-6-medium-full-outer-discrepancy.md", """# Activity 1-6 (Medium): Discrepancy Audit with Full Outer Join

## Problem Scenario
During a post-migration audit between an on-premise ERP system and a cloud-based Warehouse Management System (WMS), discrepancies have appeared in logistics billing. The ERP stores outbound shipments in `legacy_shipments`, while the WMS records billed carrier receipts in `platform_receipts`. The financial auditor needs a reconciliation audit report showing every tracking number present in either or both systems, along with the ERP cost, the platform billed amount, and an audit status classifying whether the record is 'Matched', 'Missing in Platform', or 'Missing in Legacy'.

### Data Schema Overview
- **`legacy_shipments` Table**: `tracking_number` (VARCHAR), `erp_cost` (DECIMAL), `shipper_name` (VARCHAR)
- **`platform_receipts` Table**: `tracking_number` (VARCHAR), `billed_amount` (DECIMAL), `carrier_status` (VARCHAR)

### Objectives
1. Perform a full outer join ($A \\cup B$) to capture tracking numbers from both systems.
2. Align tracking numbers using `COALESCE`.
3. Categorize the audit status:
   - 'Matched' if present in both.
   - 'Missing in Platform' if only in legacy.
   - 'Missing in Legacy' if only in platform receipts.
4. Order by tracking number ascending.

## Hints
- A full outer join preserves unmatched rows from both sides, producing NULL values whenever a key exists in one table but not the other.
- Use `CASE WHEN` in SQL and `np.select` (or conditional lambda/masking) in Python to assign the audit status based on NULL checks.
""")

write_sol("sol1-6-medium-full-outer-discrepancy.md", """# Solution 1-6 (Medium): Discrepancy Audit with Full Outer Join

## SQL Implementation
```sql
SELECT 
    -- Reason: Coalesce tracking numbers so we always have a non-null key regardless of which side matched
    COALESCE(l.tracking_number, p.tracking_number) AS tracking_number,
    l.erp_cost,
    p.billed_amount,
    -- Reason: Classify audit status based on existence of keys in respective tables
    CASE 
        WHEN l.tracking_number IS NOT NULL AND p.tracking_number IS NOT NULL THEN 'Matched'
        WHEN l.tracking_number IS NOT NULL AND p.tracking_number IS NULL THEN 'Missing in Platform'
        ELSE 'Missing in Legacy'
    END AS audit_status
FROM legacy_shipments l
-- Reason: FULL OUTER JOIN returns all rows from both tables ($A \\cup B$)
FULL OUTER JOIN platform_receipts p 
    ON l.tracking_number = p.tracking_number
ORDER BY tracking_number ASC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

legacy_shipments = pd.DataFrame({
    'tracking_number': ['TRK-1001', 'TRK-1002', 'TRK-1003', 'TRK-1004', 'TRK-1005'],
    'erp_cost': [45.50, 120.00, 85.20, 33.10, 210.00],
    'shipper_name': ['FedEx', 'UPS', 'DHL', 'USPS', 'FreightOne']
})

platform_receipts = pd.DataFrame({
    'tracking_number': ['TRK-1001', 'TRK-1002', 'TRK-1003', 'TRK-1006', 'TRK-1007'],
    'billed_amount': [45.50, 125.00, 85.20, 74.00, 150.00],
    'carrier_status': ['Delivered', 'Delivered', 'In Transit', 'Delivered', 'Exception']
})

# Reason: how='outer' executes a full outer join aligning matching tracking numbers
merged_df = pd.merge(
    legacy_shipments, 
    platform_receipts, 
    on='tracking_number', 
    how='outer', 
    suffixes=('_legacy', '_platform')
)

# Reason: Define vectorized conditions to classify discrepancies
conditions = [
    merged_df['erp_cost'].notna() & merged_df['billed_amount'].notna(),
    merged_df['erp_cost'].notna() & merged_df['billed_amount'].isna(),
    merged_df['erp_cost'].isna() & merged_df['billed_amount'].notna()
]
choices = ['Matched', 'Missing in Platform', 'Missing in Legacy']

merged_df['audit_status'] = np.select(conditions, choices, default='Unknown')

result_df = merged_df[['tracking_number', 'erp_cost', 'billed_amount', 'audit_status']].sort_values(by='tracking_number', ascending=True)
print(result_df)
```
""")

# 1-7 Medium: Union All Log Stacking
write_act("act1-7-medium-union-all-log-stacking.md", """# Activity 1-7 (Medium): Unifying Web and Mobile Event Streams

## Problem Scenario
A product analytics team monitors engagement across two independent channels: desktop web sessions stored in `web_clicks` and native smartphone interactions stored in `mobile_taps`. To run cross-platform user journey analyses, the data engineering team needs to stack these two event streams into a single unified event timeline. The resulting dataset must normalize column names, add a source platform flag (`'WEB'` vs `'MOBILE'`), and present all interactions chronologically.

### Data Schema Overview
- **`web_clicks` Table**: `event_id` (VARCHAR), `user_id` (INT), `action_type` (VARCHAR), `event_timestamp` (VARCHAR)
- **`mobile_taps` Table**: `event_id` (VARCHAR), `user_id` (INT), `action_type` (VARCHAR), `event_timestamp` (VARCHAR)

### Objectives
1. Combine records from both tables without discarding duplicate user actions using set stacking (`UNION ALL`).
2. Add a literal discriminator column `platform` (`'WEB'` or `'MOBILE'`).
3. Output `event_id`, `user_id`, `platform`, `action_type`, and `event_timestamp`.
4. Order by `event_timestamp` ascending.

## Hints
- `UNION ALL` stacks rows from multiple result sets without the performance overhead of deduplicating records.
- In Pandas, vertical concatenation is achieved using `pd.concat()`, passing an array of DataFrames with matching schema columns.
""")

write_sol("sol1-7-medium-union-all-log-stacking.md", """# Solution 1-7 (Medium): Unifying Web and Mobile Event Streams

## SQL Implementation
```sql
-- Query 1: Extract web events with literal platform tag
SELECT 
    event_id,
    user_id,
    'WEB' AS platform,
    action_type,
    event_timestamp
FROM web_clicks

UNION ALL

-- Reason: UNION ALL concatenates rows directly without performing an expensive distinct sort
-- Query 2: Extract mobile events with literal platform tag
SELECT 
    event_id,
    user_id,
    'MOBILE' AS platform,
    action_type,
    event_timestamp
FROM mobile_taps

-- Reason: Sort combined event stream chronologically
ORDER BY event_timestamp ASC;
```

## Python Implementation
```python
import pandas as pd

web_clicks = pd.DataFrame({
    'event_id': ['WEB-01', 'WEB-02', 'WEB-03', 'WEB-04'],
    'user_id': [101, 102, 101, 103],
    'action_type': ['page_view', 'add_to_cart', 'checkout_start', 'page_view'],
    'event_timestamp': ['2024-03-01 10:01:05', '2024-03-01 10:05:12', '2024-03-01 10:12:44', '2024-03-01 10:15:30']
})

mobile_taps = pd.DataFrame({
    'event_id': ['MOB-01', 'MOB-02', 'MOB-03', 'MOB-04'],
    'user_id': [102, 104, 101, 102],
    'action_type': ['app_open', 'page_view', 'push_dismiss', 'checkout_success'],
    'event_timestamp': ['2024-03-01 10:00:20', '2024-03-01 10:04:15', '2024-03-01 10:11:00', '2024-03-01 10:20:00']
})

# Reason: Assign literal platform tags to match SQL query structure
web_clicks['platform'] = 'WEB'
mobile_taps['platform'] = 'MOBILE'

# Reason: pd.concat with axis=0 performs SQL UNION ALL equivalent
unified_events = pd.concat([web_clicks, mobile_taps], axis=0, ignore_index=True)

# Reason: Sort chronologically across the unified platform timeline
unified_events = unified_events.sort_values(by='event_timestamp', ascending=True)

print(unified_events)
```
""")

# 1-8 Medium: Conditional Aggregations
write_act("act1-8-medium-conditional-aggregations.md", """# Activity 1-8 (Medium): Payment Channel Breakdown & Settlement

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
""")

write_sol("sol1-8-medium-conditional-aggregations.md", """# Solution 1-8 (Medium): Payment Channel Breakdown & Settlement

## SQL Implementation
```sql
SELECT 
    payment_method,
    -- Reason: Count total attempted transactions
    COUNT(txn_id) AS total_attempts,
    -- Reason: Count distinct customers who utilized this payment channel
    COUNT(DISTINCT customer_id) AS unique_customers,
    -- Reason: Conditional SUM calculates settled revenue only for completed transactions
    COALESCE(SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END), 0.00) AS completed_volume,
    -- Reason: Conditional SUM/COUNT counts records where status is Refunded
    SUM(CASE WHEN status = 'Refunded' THEN 1 ELSE 0 END) AS refunded_count
FROM transactions
GROUP BY payment_method
ORDER BY completed_volume DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

transactions = pd.DataFrame({
    'txn_id': ['TXN-01', 'TXN-02', 'TXN-03', 'TXN-04', 'TXN-05', 'TXN-06', 'TXN-07', 'TXN-08', 'TXN-09'],
    'customer_id': [1, 2, 1, 3, 4, 2, 5, 3, 1],
    'payment_method': ['Credit Card', 'PayPal', 'Credit Card', 'Bank Wire', 'Credit Card', 'PayPal', 'Apple Pay', 'Bank Wire', 'Apple Pay'],
    'amount': [150.00, 80.00, 200.00, 1200.00, 50.00, 120.00, 95.00, 3400.00, 40.00],
    'status': ['Completed', 'Completed', 'Completed', 'Completed', 'Refunded', 'Completed', 'Completed', 'Completed', 'Completed']
})

# Reason: Create vectorized helper columns for conditional aggregation
transactions['completed_amount'] = np.where(transactions['status'] == 'Completed', transactions['amount'], 0.0)
transactions['is_refunded'] = np.where(transactions['status'] == 'Refunded', 1, 0)

# Reason: Group by payment_method and aggregate metrics
channel_summary = transactions.groupby('payment_method').agg(
    total_attempts=('txn_id', 'count'),
    unique_customers=('customer_id', 'nunique'),
    completed_volume=('completed_amount', np.sum),
    refunded_count=('is_refunded', np.sum)
).reset_index()

channel_summary = channel_summary.sort_values(by='completed_volume', ascending=False)
print(channel_summary)
```
""")

# 1-9 Hard: Multi-Tier Customer Spend
write_act("act1-9-hard-multi-tier-customer-spend.md", """# Activity 1-9 (Hard): Multi-Tier Customer Line-Item Synthesis

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
""")

write_sol("sol1-9-hard-multi-tier-customer-spend.md", """# Solution 1-9 (Hard): Multi-Tier Customer Line-Item Synthesis

## SQL Implementation
```sql
SELECT 
    c.customer_id,
    c.name,
    c.tier,
    -- Reason: Count distinct orders placed by the customer
    COUNT(DISTINCT o.order_id) AS total_orders_placed,
    -- Reason: Sum total quantity of items ordered; COALESCE handles inactive clients
    COALESCE(SUM(oi.quantity), 0) AS total_units_purchased,
    -- Reason: Compute total spending across all line items
    COALESCE(SUM(oi.quantity * oi.unit_price), 0.00) AS total_expenditure
FROM customers c
-- Reason: Chain LEFT JOINs starting from the root entity (customers)
-- Using INNER JOIN here would drop inactive clients like Delta Health and Epsilon Retail
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id
LEFT JOIN order_items oi 
    ON o.order_id = oi.order_id
LEFT JOIN products p 
    ON oi.product_id = p.product_id
GROUP BY c.customer_id, c.name, c.tier
ORDER BY total_expenditure DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['Alpha Corp', 'Beta Tech', 'Gamma LLC', 'Delta Health', 'Epsilon Retail'],
    'tier': ['Gold', 'Silver', 'Bronze', 'Gold', 'Bronze']
})

orders = pd.DataFrame({
    'order_id': [5001, 5002, 5003, 5004],
    'customer_id': [1, 1, 2, 3],
    'order_date': ['2024-01-15', '2024-02-10', '2024-01-20', '2024-02-12']
})

products = pd.DataFrame({
    'product_id': [101, 102, 103, 104],
    'product_name': ['Cloud Server Blade', 'Network Switch 48P', 'SaaS Annual Seat', 'Support Ticket Pack'],
    'category': ['Infrastructure', 'Networking', 'Software', 'Services']
})

order_items = pd.DataFrame({
    'item_id': [1, 2, 3, 4, 5],
    'order_id': [5001, 5001, 5002, 5003, 5004],
    'product_id': [101, 102, 103, 104, 101],
    'quantity': [2, 1, 5, 2, 1],
    'unit_price': [1500.00, 800.00, 250.00, 400.00, 1500.00]
})

# Reason: Sequential left joins to guarantee customer retention
df_merged = pd.merge(customers, orders, on='customer_id', how='left')
df_merged = pd.merge(df_merged, order_items, on='order_id', how='left')
df_merged = pd.merge(df_merged, products, on='product_id', how='left')

# Reason: Calculate line item total value with vectorized multiplication
df_merged['line_total'] = df_merged['quantity'] * df_merged['unit_price']

# Reason: Aggregate per customer entity
customer_report = df_merged.groupby(['customer_id', 'name', 'tier']).agg(
    total_orders_placed=('order_id', 'nunique'),
    total_units_purchased=('quantity', np.sum),
    total_expenditure=('line_total', np.sum)
).reset_index()

# Reason: Resolve NaNs introduced by left-join misses
customer_report['total_units_purchased'] = customer_report['total_units_purchased'].fillna(0).astype(int)
customer_report['total_expenditure'] = customer_report['total_expenditure'].fillna(0.00)

customer_report = customer_report.sort_values(by='total_expenditure', ascending=False)
print(customer_report)
```
""")

# 1-10 Hard: Normalized Inventory Reconciliation
write_act("act1-10-hard-normalized-inventory-reconciliation.md", """# Activity 1-10 (Hard): Multi-Channel Inventory Reconciliation Audit

## Problem Scenario
An international logistics warehouse reconciles hardware assets by comparing inbound supplier deliveries in `purchase_receipts` against outbound customer dispatches in `sales_shipments`, grounded by an overarching master product list in `current_catalog`. 

The inventory control director requires a master stock audit report for **every single SKU** in the catalog. The report must calculate total inbound received units, total outbound shipped units, the net balance on hand (`total_received - total_shipped`), and the total net asset value (`net_balance * base_cost`). Inactive SKUs with zero movement must be preserved with a balance and valuation of 0.

### Data Schema Overview
- **`current_catalog` Table**: `sku` (VARCHAR), `sku_name` (VARCHAR), `base_cost` (DECIMAL)
- **`purchase_receipts` Table**: `receipt_id` (INT), `sku` (VARCHAR), `quantity_received` (INT)
- **`sales_shipments` Table**: `shipment_id` (INT), `sku` (VARCHAR), `quantity_shipped` (INT)

### Objectives
1. Synthesize inbound receipts and outbound shipments without producing cartesian cross-product multiplication errors.
2. Ensure SKUs with zero transactions (such as `SKU-E`) are preserved in the catalog.
3. Compute `total_received`, `total_shipped`, `net_balance`, and `inventory_valuation`.
4. Order by `inventory_valuation` descending.

## Hints
- Warning: Joining `purchase_receipts` directly to `sales_shipments` on `sku` creates a duplicate multiplication trap (fan-out) if a SKU has multiple receipts and multiple shipments!
- Pre-aggregate inbound receipts and outbound shipments by `sku` separately, or join aggregated subqueries/DataFrames back to `current_catalog`.
""")

write_sol("sol1-10-hard-normalized-inventory-reconciliation.md", """# Solution 1-10 (Hard): Multi-Channel Inventory Reconciliation Audit

## SQL Implementation
```sql
-- Step 1: Pre-aggregate inbound receipts per SKU to avoid Cartesian fan-out join traps
WITH receipts_summary AS (
    SELECT sku, SUM(quantity_received) AS total_received
    FROM purchase_receipts
    GROUP BY sku
),
-- Step 2: Pre-aggregate outbound shipments per SKU
shipments_summary AS (
    SELECT sku, SUM(quantity_shipped) AS total_shipped
    FROM sales_shipments
    GROUP BY sku
)
-- Step 3: Synthesize master catalog with pre-aggregated metrics
SELECT 
    c.sku,
    c.sku_name,
    c.base_cost,
    COALESCE(r.total_received, 0) AS total_received,
    COALESCE(s.total_shipped, 0) AS total_shipped,
    -- Reason: Net balance calculation handling NULL fallbacks
    (COALESCE(r.total_received, 0) - COALESCE(s.total_shipped, 0)) AS net_balance,
    -- Reason: Asset valuation based on net on-hand units
    (COALESCE(r.total_received, 0) - COALESCE(s.total_shipped, 0)) * c.base_cost AS inventory_valuation
FROM current_catalog c
LEFT JOIN receipts_summary r ON c.sku = r.sku
LEFT JOIN shipments_summary s ON c.sku = s.sku
ORDER BY inventory_valuation DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

catalog = pd.DataFrame({
    'sku': ['SKU-A', 'SKU-B', 'SKU-C', 'SKU-D', 'SKU-E'],
    'sku_name': ['Industrial Router', 'Optical Transceiver', 'Patch Panel Cat6', 'Server Rack 42U', 'Power Distribution Unit'],
    'base_cost': [180.00, 45.00, 60.00, 650.00, 120.00]
})

purchase_receipts = pd.DataFrame({
    'receipt_id': [1, 2, 3, 4, 5],
    'sku': ['SKU-A', 'SKU-A', 'SKU-B', 'SKU-C', 'SKU-D'],
    'quantity_received': [50, 30, 200, 80, 10]
})

sales_shipments = pd.DataFrame({
    'shipment_id': [101, 102, 103, 104],
    'sku': ['SKU-A', 'SKU-B', 'SKU-C', 'SKU-D'],
    'quantity_shipped': [40, 150, 75, 8]
})

# Reason: Pre-aggregate receipts and shipments to avoid cartesian row explosion
rec_agg = purchase_receipts.groupby('sku')['quantity_received'].sum().reset_index(name='total_received')
ship_agg = sales_shipments.groupby('sku')['quantity_shipped'].sum().reset_index(name='total_shipped')

# Reason: Left merge pre-aggregated metrics to master catalog
reconciled = pd.merge(catalog, rec_agg, on='sku', how='left')
reconciled = pd.merge(reconciled, ship_agg, on='sku', how='left')

# Reason: Resolve missing movements to 0
reconciled['total_received'] = reconciled['total_received'].fillna(0).astype(int)
reconciled['total_shipped'] = reconciled['total_shipped'].fillna(0).astype(int)

# Reason: Vectorized calculation of net balance and valuation
reconciled['net_balance'] = reconciled['total_received'] - reconciled['total_shipped']
reconciled['inventory_valuation'] = reconciled['net_balance'] * reconciled['base_cost']

reconciled = reconciled.sort_values(by='inventory_valuation', ascending=False)
print(reconciled)
```
""")

print("Unit 1 generation complete.")
