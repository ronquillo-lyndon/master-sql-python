"""
Script to generate all 10 Unit 3 Activity and Solution markdown files.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACT_DIR = os.path.join(BASE_DIR, "practice-activities")
SOL_DIR = os.path.join(BASE_DIR, "practice-activities-solution")

def write_act(filename, content):
    filepath = os.path.join(ACT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def write_sol(filename, content):
    filepath = os.path.join(SOL_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print("Generating Unit 3 Activities and Solutions...")

# ==========================================
# UNIT 3
# ==========================================

# 3-1 Easy: Text Trim Casing
write_act("act3-1-easy-text-trim-casing.md", """# Activity 3-1 (Easy): Ingestion Cleansing of Dirty User Strings

## Problem Scenario
A customer onboarding intake form writes raw, unvalidated entries directly into a `raw_leads` staging table. Marketing analysts report that leading and trailing whitespace, inconsistent casing in email addresses, and unstandardized country codes are breaking downstream email automation campaigns. 

The data engineering pipeline must clean this raw table by:
1. Stripping all leading and trailing whitespace from names and email addresses.
2. Converting all email addresses to lowercase.
3. Standardizing all country names to uppercase.
4. Converting customer names to title case (capitalizing the first letter of each word).

### Data Schema Overview
- **`raw_leads` Table**: `lead_id` (INT), `raw_name` (VARCHAR), `raw_email` (VARCHAR), `country` (VARCHAR)

### Objectives
1. Use SQL string formatting functions (`TRIM`, `LOWER`, `UPPER`).
2. In Python, use vectorized or lambda string transformations (`.strip()`, `.lower()`, `.title()`).
3. Output `lead_id`, `cleaned_name`, `cleaned_email`, and `standardized_country`.
4. Order by `lead_id` ascending.

## Hints
- SQL provides standard string functions like `TRIM()`, `LOWER()`, and `UPPER()`. Title casing can be handled with built-in functions or application-layer Python lambdas.
- In Python, apply string methods across DataFrame columns using `.str.strip()`, `.str.lower()`, or `.apply(lambda x: ...)`.
""")

write_sol("sol3-1-easy-text-trim-casing.md", """# Solution 3-1 (Easy): Ingestion Cleansing of Dirty User Strings

## SQL Implementation
```sql
SELECT 
    lead_id,
    -- Reason: TRIM removes accidental leading and trailing whitespace.
    -- (In standard SQL, UPPER/LOWER handles casing; database extensions or Python handle title-casing).
    TRIM(raw_name) AS cleaned_name,
    -- Reason: Lowercase emails to prevent duplicate account lookup errors
    TRIM(LOWER(raw_email)) AS cleaned_email,
    -- Reason: Standardize country to uniform uppercase format (e.g. 'USA')
    TRIM(UPPER(country)) AS standardized_country
FROM raw_leads
ORDER BY lead_id ASC;
```

## Python Implementation
```python
import pandas as pd

raw_leads = pd.DataFrame({
    'lead_id': [1, 2, 3, 4, 5],
    'raw_name': ['   ALEXANDER SMITH  ', 'maria garcia', '  KEVIN TRAN  ', ' Sarah Connor ', 'david  lee'],
    'raw_email': ['ALEX@EXAMPLE.COM   ', '   Maria.Garcia@Domain.Org', 'kevin.tran@company.io', '  SARAH.C@SKY.NET ', 'DAVID.LEE@WEBMAIL.COM'],
    'country': ['USA', 'spain', 'VIETNAM', 'usa', 'Canada']
})

# Reason: Replicate programmatic pre-processing using Lambda and vectorized string functions
# 1. Clean and Title-Case customer names
raw_leads['cleaned_name'] = raw_leads['raw_name'].apply(lambda x: str(x).strip().title())

# 2. Strip whitespace and lowercase emails
raw_leads['cleaned_email'] = raw_leads['raw_email'].apply(lambda x: str(x).strip().lower())

# 3. Strip whitespace and uppercase country names
raw_leads['standardized_country'] = raw_leads['country'].apply(lambda x: str(x).strip().upper())

result_df = raw_leads[['lead_id', 'cleaned_name', 'cleaned_email', 'standardized_country']].sort_values(by='lead_id')
print(result_df)
```
""")

# 3-2 Easy: Null Coalesce Imputation
write_act("act3-2-easy-null-coalesce-imputation.md", """# Activity 3-2 (Easy): Logistics Freight Surcharge Fallback Imputation

## Problem Scenario
A freight management company records delivery invoice line items in `shipment_costs`. Because fuel surcharges and expedite fees are optional add-ons, carrier systems frequently transmit `NULL` values instead of zero dollars for unassessed fees. If an arithmetic addition is performed directly on columns containing `NULL`, standard relational and programmatic math evaluates the entire sum to `NULL`, resulting in missing invoice totals.

The billing department needs a report calculating the total invoice cost (`base_cost + fuel_surcharge + expedite_fee`), ensuring that missing surcharges safely default to `$0.00`.

### Data Schema Overview
- **`shipment_costs` Table**: `shipment_id` (VARCHAR), `base_cost` (DECIMAL), `fuel_surcharge` (DECIMAL), `expedite_fee` (DECIMAL)

### Objectives
1. Fallback missing `fuel_surcharge` to `0.00`.
2. Fallback missing `expedite_fee` to `0.00`.
3. Compute `total_invoice_cost`.
4. Order the output by `total_invoice_cost` descending.

## Hints
- In SQL, `COALESCE(val, fallback)` returns the first non-null argument.
- In Pandas, replace NaNs using `.fillna(0.00)` before performing column addition.
""")

write_sol("sol3-2-easy-null-coalesce-imputation.md", """# Solution 3-2 (Easy): Logistics Freight Surcharge Fallback Imputation

## SQL Implementation
```sql
SELECT 
    shipment_id,
    base_cost,
    -- Reason: Replace NULL surcharges with 0.00 to avoid arithmetic poison where NULL + X = NULL
    COALESCE(fuel_surcharge, 0.00) AS imputed_fuel_surcharge,
    COALESCE(expedite_fee, 0.00) AS imputed_expedite_fee,
    -- Reason: Safely calculate total invoice cost using coalesced values
    base_cost + COALESCE(fuel_surcharge, 0.00) + COALESCE(expedite_fee, 0.00) AS total_invoice_cost
FROM shipment_costs
ORDER BY total_invoice_cost DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

shipment_costs = pd.DataFrame({
    'shipment_id': ['SHP-001', 'SHP-002', 'SHP-003', 'SHP-004', 'SHP-005'],
    'base_cost': [250.00, 400.00, 180.00, 520.00, 310.00],
    'fuel_surcharge': [35.00, np.nan, 20.00, np.nan, 45.00],
    'expedite_fee': [50.00, 0.00, np.nan, np.nan, 25.00]
})

# Reason: Inspect missingness volume for quality control
missing_fuel = shipment_costs['fuel_surcharge'].isna().sum()
missing_expedite = shipment_costs['expedite_fee'].isna().sum()
print(f"[QC] Found {missing_fuel} missing fuel surcharges and {missing_expedite} missing expedite fees.")

# Reason: Default optional add-on fees to 0.00
shipment_costs['fuel_surcharge'] = shipment_costs['fuel_surcharge'].fillna(0.00)
shipment_costs['expedite_fee'] = shipment_costs['expedite_fee'].fillna(0.00)

# Reason: Perform vectorized column addition to compute total invoice cost
shipment_costs['total_invoice_cost'] = (
    shipment_costs['base_cost'] + 
    shipment_costs['fuel_surcharge'] + 
    shipment_costs['expedite_fee']
)

result_df = shipment_costs.sort_values(by='total_invoice_cost', ascending=False)
print(result_df)
```
""")

# 3-3 Easy: Row Deduplication
write_act("act3-3-easy-row-deduplication.md", """# Activity 3-3 (Easy): Payment Webhook Deduplication Pipeline

## Problem Scenario
Payment gateway webhooks stream real-time settlement notices into `payment_webhooks`. Due to network retries, duplicate delivery attempts frequently insert multiple identical event notifications with the same `event_id` and transaction reference `txn_ref`, but differing `record_id` and slight timestamp variances. 

The accounting pipeline must filter out all duplicate webhook delivery attempts, retaining strictly the **first** received event per `event_id`.

### Data Schema Overview
- **`payment_webhooks` Table**: `record_id` (INT), `event_id` (VARCHAR), `txn_ref` (VARCHAR), `amount` (DECIMAL), `received_at` (TIMESTAMP)

### Objectives
1. Identify records that share identical `event_id` keys.
2. In SQL, use `ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY received_at ASC)` inside a CTE or subquery and filter for `row_num = 1`.
3. In Python, apply `.drop_duplicates(subset=['event_id'], keep='first')`.
4. Order the clean output by `record_id` ascending.

## Hints
- When duplicate rows differ by a metadata field (such as `received_at` or auto-incrementing ID), standard `SELECT DISTINCT *` fails. Instead, use partitioned ranking or dedicated deduplication methods.
- In Pandas, `.drop_duplicates()` with `keep='first'` requires the DataFrame to be pre-sorted by the desired timestamp order.
""")

write_sol("sol3-3-easy-row-deduplication.md", """# Solution 3-3 (Easy): Payment Webhook Deduplication Pipeline

## SQL Implementation
```sql
WITH ranked_webhooks AS (
    SELECT 
        record_id,
        event_id,
        txn_ref,
        amount,
        received_at,
        -- Reason: Enumerate occurrences per event_id chronologically
        ROW_NUMBER() OVER (
            PARTITION BY event_id 
            ORDER BY received_at ASC
        ) AS delivery_attempt
    FROM payment_webhooks
)
-- Reason: Retain only the initial webhook notification (attempt #1)
SELECT 
    record_id,
    event_id,
    txn_ref,
    amount,
    received_at
FROM ranked_webhooks
WHERE delivery_attempt = 1
ORDER BY record_id ASC;
```

## Python Implementation
```python
import pandas as pd

payment_webhooks = pd.DataFrame({
    'record_id': [1, 2, 3, 4, 5],
    'event_id': ['EVT-101', 'EVT-101', 'EVT-102', 'EVT-103', 'EVT-103'],
    'txn_ref': ['TXN-9001', 'TXN-9001', 'TXN-9002', 'TXN-9003', 'TXN-9003'],
    'amount': [120.50, 120.50, 85.00, 340.00, 340.00],
    'received_at': ['2024-03-01 12:00:01', '2024-03-01 12:00:03', '2024-03-01 12:05:10', '2024-03-01 12:10:00', '2024-03-01 12:10:02']
})

payment_webhooks['received_at'] = pd.to_datetime(payment_webhooks['received_at'])

# Reason: Ensure dataset is strictly sorted by arrival timestamp before deduplication
payment_webhooks = payment_webhooks.sort_values(by='received_at').reset_index(drop=True)

# Reason: Check duplicate volume for pipeline telemetry
duplicate_count = payment_webhooks.duplicated(subset=['event_id']).sum()
print(f"[QC] Dropping {duplicate_count} duplicate webhook delivery attempt(s).")

# Reason: Replicate SQL WHERE row_num = 1 using drop_duplicates keep='first'
clean_webhooks = payment_webhooks.drop_duplicates(subset=['event_id'], keep='first').sort_values(by='record_id')

print(clean_webhooks)
```
""")

# 3-4 Easy: Type Casting Dates
write_act("act3-4-easy-type-casting-dates.md", """# Activity 3-4 (Easy): Type Ingestion: Parsing Untyped Raw Invoices

## Problem Scenario
An ingestion pipeline loads raw vendor CSV invoices into `raw_staging_invoices`. Because CSV formats do not enforce typing, both transaction dates (`string_date`) and monetary amounts (`raw_amount_str`) were ingested as raw strings (e.g. `'2024-01-15'` and `'1450.50'`). Before downstream financial modeling or date-based partitioning can occur, the data engineer must cast these strings into native SQL `DATE` and `DECIMAL` types.

### Data Schema Overview
- **`raw_staging_invoices` Table**: `invoice_id` (VARCHAR), `string_date` (VARCHAR), `raw_amount_str` (VARCHAR)

### Objectives
1. Cast `string_date` to an authentic `DATE` type.
2. Cast `raw_amount_str` to a `DECIMAL(10, 2)` or `FLOAT` type.
3. Compute a calculated column `sales_tax` as 8% (`amount * 0.08`), rounded to two decimal places.
4. Order the output by `invoice_date` ascending.

## Hints
- In SQL, use `CAST(column AS DATE)` and `CAST(column AS DECIMAL(10, 2))`.
- In Pandas, convert dates using `pd.to_datetime()` and numeric strings using `.astype(float)`.
""")

write_sol("sol3-4-easy-type-casting-dates.md", """# Solution 3-4 (Easy): Type Ingestion: Parsing Untyped Raw Invoices

## SQL Implementation
```sql
SELECT 
    invoice_id,
    -- Reason: Cast string date to native SQL DATE for proper temporal ordering and indexing
    CAST(string_date AS DATE) AS invoice_date,
    -- Reason: Cast string amount to numerical DECIMAL for accurate arithmetic
    CAST(raw_amount_str AS DECIMAL(10, 2)) AS amount,
    -- Reason: Compute derived tax calculation on properly typed numerical column
    ROUND(CAST(raw_amount_str AS DECIMAL(10, 2)) * 0.08, 2) AS sales_tax
FROM raw_staging_invoices
ORDER BY invoice_date ASC;
```

## Python Implementation
```python
import pandas as pd

raw_staging_invoices = pd.DataFrame({
    'invoice_id': ['INV-801', 'INV-802', 'INV-803', 'INV-804', 'INV-805'],
    'string_date': ['2024-01-15', '2024-01-16', '2024-01-20', '2024-01-22', '2024-01-25'],
    'raw_amount_str': ['1450.50', '320.00', '890.75', '1100.00', '45.25']
})

# Reason: Parse string dates to datetime64 type
raw_staging_invoices['invoice_date'] = pd.to_datetime(raw_staging_invoices['string_date'])

# Reason: Cast string numbers to float64 for mathematical operations
raw_staging_invoices['amount'] = raw_staging_invoices['raw_amount_str'].astype(float)

# Reason: Vectorized calculation of derived tax metric
raw_staging_invoices['sales_tax'] = (raw_staging_invoices['amount'] * 0.08).round(2)

result_df = raw_staging_invoices[['invoice_id', 'invoice_date', 'amount', 'sales_tax']].sort_values(by='invoice_date')
print(result_df)
```
""")

# 3-5 Medium: Conditional Case When
write_act("act3-5-medium-conditional-case-when.md", """# Activity 3-5 (Medium): Customer Retention Segmentation with CASE WHEN

## Problem Scenario
The customer success team uses `customer_activity` to monitor user health. Analysts need to assign every customer to an actionable engagement tier based on business logic:
- **`VIP Active`**: `lifetime_spend >= 20000.00` AND `days_since_last_login <= 30`
- **`VIP Churn Risk`**: `lifetime_spend >= 20000.00` AND `days_since_last_login > 30`
- **`Standard Active`**: `lifetime_spend < 20000.00` AND `days_since_last_login <= 30`
- **`Standard Dormant`**: `lifetime_spend < 20000.00` AND `days_since_last_login > 30`

The report must output each customer, their current metrics, and their evaluated `account_health_tier`.

### Data Schema Overview
- **`customer_activity` Table**: `customer_id` (INT), `company_name` (VARCHAR), `lifetime_spend` (DECIMAL), `days_since_last_login` (INT)

### Objectives
1. Implement multi-branch conditional classification logic using `CASE WHEN ... THEN ... ELSE ... END`.
2. In Python, implement vectorized condition evaluation using `np.select`.
3. Order the resulting report by `lifetime_spend` descending.

## Hints
- `CASE WHEN` evaluates conditions sequentially from top to bottom; the first true branch is returned.
- In Python, `np.select(conditions, choices, default=...)` provides a clean, vectorized equivalent to SQL `CASE WHEN`.
""")

write_sol("sol3-5-medium-conditional-case-when.md", """# Solution 3-5 (Medium): Customer Retention Segmentation with CASE WHEN

## SQL Implementation
```sql
SELECT 
    customer_id,
    company_name,
    lifetime_spend,
    days_since_last_login,
    -- Reason: Conditional branching evaluates customer value and engagement tiers
    CASE 
        WHEN lifetime_spend >= 20000.00 AND days_since_last_login <= 30 THEN 'VIP Active'
        WHEN lifetime_spend >= 20000.00 AND days_since_last_login > 30 THEN 'VIP Churn Risk'
        WHEN lifetime_spend < 20000.00 AND days_since_last_login <= 30 THEN 'Standard Active'
        ELSE 'Standard Dormant'
    END AS account_health_tier
FROM customer_activity
ORDER BY lifetime_spend DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

customer_activity = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5, 6],
    'company_name': ['Alpha Tech', 'Beta Logistics', 'Gamma Global', 'Delta Dynamics', 'Epsilon Retail', 'Zeta Health'],
    'lifetime_spend': [25000.00, 4500.00, 85000.00, 800.00, 12000.00, 500.00],
    'days_since_last_login': [4, 45, 2, 120, 18, 5]
})

# Reason: Define vectorized conditions and matching choices matching SQL CASE WHEN
conditions = [
    (customer_activity['lifetime_spend'] >= 20000.00) & (customer_activity['days_since_last_login'] <= 30),
    (customer_activity['lifetime_spend'] >= 20000.00) & (customer_activity['days_since_last_login'] > 30),
    (customer_activity['lifetime_spend'] < 20000.00) & (customer_activity['days_since_last_login'] <= 30),
    (customer_activity['lifetime_spend'] < 20000.00) & (customer_activity['days_since_last_login'] > 30)
]

choices = ['VIP Active', 'VIP Churn Risk', 'Standard Active', 'Standard Dormant']

customer_activity['account_health_tier'] = np.select(conditions, choices, default='Unclassified')

result_df = customer_activity.sort_values(by='lifetime_spend', ascending=False)
print(result_df)
```
""")

# 3-6 Medium: Median Imputation Pandas
write_act("act3-6-medium-median-imputation-pandas.md", """# Activity 3-6 (Medium): Skew-Resistant Median Imputation

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
""")

write_sol("sol3-6-medium-median-imputation-pandas.md", """# Solution 3-6 (Medium): Skew-Resistant Median Imputation

## Python Implementation (Pandas Imputation Pipeline)
```python
import pandas as pd
import numpy as np

delivery_performance = pd.DataFrame({
    'delivery_id': ['DEL-01', 'DEL-02', 'DEL-03', 'DEL-04', 'DEL-05', 'DEL-06', 'DEL-07', 'DEL-08'],
    'carrier': ['SpeedyFreight'] * 8,
    'transit_days': [2.0, 3.0, 2.5, np.nan, 19.0, 3.0, np.nan, 2.8]
})

# Reason: 1. Quality control check - identify missingness volume
missing_count = delivery_performance['transit_days'].isna().sum()
print(f"[QC] Detected {missing_count} missing delivery records.")

# Reason: 2. Calculate median (robust against the 19.0 outlier skew)
computed_median = delivery_performance['transit_days'].median()
print(f"[Imputation] Computed Median: {computed_median:.2f} days (vs Mean: {delivery_performance['transit_days'].mean():.2f} days)")

# Reason: 3. Create boolean flag identifying imputed records before filling
delivery_performance['is_imputed'] = delivery_performance['transit_days'].isna()

# Reason: 4. Impute missing slots with computed median
delivery_performance['cleaned_transit_days'] = delivery_performance['transit_days'].fillna(computed_median)

print(delivery_performance[['delivery_id', 'carrier', 'cleaned_transit_days', 'is_imputed']])
```

## SQL Implementation (DuckDB / Analytical SQL)
```sql
WITH median_calc AS (
    -- Reason: Calculate median transit time across valid observations
    SELECT MEDIAN(transit_days) AS median_transit
    FROM delivery_performance
    WHERE transit_days IS NOT NULL
)
SELECT 
    d.delivery_id,
    d.carrier,
    -- Reason: COALESCE replaces NULLs with the scalar median value from the CTE
    COALESCE(d.transit_days, m.median_transit) AS cleaned_transit_days,
    -- Reason: Boolean flag recording whether value was imputed
    CASE WHEN d.transit_days IS NULL THEN TRUE ELSE FALSE END AS is_imputed
FROM delivery_performance d
CROSS JOIN median_calc m
ORDER BY d.delivery_id ASC;
```
""")

# 3-7 Medium: DuckDB Virtual View Ingestion
write_act("act3-7-medium-duckdb-virtual-view-ingestion.md", """# Activity 3-7 (Medium): Zero-Copy DuckDB Virtual View Ingestion

## Problem Scenario
Data analysts need to run high-speed OLAP queries on a cleaned vendor catalog DataFrame stored in Python memory (`supplier_catalog`). Rather than exporting to disk or spinning up a full PostgreSQL server, the pipeline utilizes **DuckDB**. 

Demonstrate an in-process data engineering pattern:
1. Register a Pandas DataFrame as a temporary virtual view inside an in-memory DuckDB connection (`conn.register()`).
2. Execute an analytical SQL aggregation query directly against the registered virtual view to calculate:
   - Total catalog SKUs per `brand`
   - Average wholesale price per `brand`
   - Total warehouse asset valuation per `brand` (`wholesale_price * available_stock`)
3. Persist the aggregated results directly into a physical DuckDB table `brand_valuation_summary`.
4. Fetch the resulting table back into Pandas via `.fetchdf()`.

### Data Schema Overview
- **`supplier_catalog` DataFrame**: `sku` (VARCHAR), `brand` (VARCHAR), `wholesale_price` (DECIMAL), `available_stock` (INT)

### Objectives
1. Connect to DuckDB (`duckdb.connect()`).
2. Register DataFrame as a virtual view.
3. Run DDL `CREATE TABLE AS SELECT ...` aggregating metrics.
4. Retrieve results using `.fetchdf()`.

## Hints
- `duckdb.connect(':memory:')` provides an ultra-fast, local in-process analytical engine.
- `conn.register('view_name', df)` makes Python DataFrames directly queryable from standard SQL without copying memory.
""")

write_sol("sol3-7-medium-duckdb-virtual-view-ingestion.md", '''# Solution 3-7 (Medium): Zero-Copy DuckDB Virtual View Ingestion

## Python & DuckDB Implementation
```python
import pandas as pd
import duckdb

supplier_catalog = pd.DataFrame({
    'sku': ['SUP-101', 'SUP-102', 'SUP-103', 'SUP-104', 'SUP-105'],
    'brand': ['LogiPro', 'LogiPro', 'AnkerPower', 'AnkerPower', 'KeySonic'],
    'wholesale_price': [45.00, 85.50, 25.00, 65.00, 110.00],
    'available_stock': [250, 140, 500, 180, 95]
})

# Reason: 1. Initialize an in-process DuckDB analytical session
conn = duckdb.connect(database=':memory:')

# Reason: 2. Register Pandas DataFrame as an in-engine virtual view (zero-copy query interface)
conn.register('virtual_supplier_catalog', supplier_catalog)

# Reason: 3. Execute analytical SQL to aggregate and ingest into a physical DuckDB table
conn.execute("""
    CREATE TABLE brand_valuation_summary AS
    SELECT 
        brand,
        COUNT(sku) AS total_skus,
        ROUND(AVG(wholesale_price), 2) AS avg_wholesale_price,
        SUM(wholesale_price * available_stock) AS total_brand_valuation
    FROM virtual_supplier_catalog
    GROUP BY brand
    ORDER BY total_brand_valuation DESC;
""")

# Reason: 4. Validate table creation by fetching results back into Pandas
result_df = conn.execute("SELECT * FROM brand_valuation_summary;").fetchdf()

print("Ingested DuckDB Table Results:")
print(result_df)

conn.close()
```

## SQL Equivalent Query Inside DuckDB
```sql
-- Query executed inside DuckDB virtual view
CREATE TABLE brand_valuation_summary AS
SELECT 
    brand,
    COUNT(sku) AS total_skus,
    ROUND(AVG(wholesale_price), 2) AS avg_wholesale_price,
    SUM(wholesale_price * available_stock) AS total_brand_valuation
FROM virtual_supplier_catalog
GROUP BY brand
ORDER BY total_brand_valuation DESC;
```
''')

# 3-8 Medium: Idempotent Table Creation
write_act("act3-8-medium-idempotent-table-creation.md", """# Activity 3-8 (Medium): Building Idempotent Ingestion Pipelines

## Problem Scenario
In production data engineering, pipelines are scheduled to run on recurring schedules (e.g. hourly or daily). If an orchestrator triggers a retry due to a transient network hiccup, a non-idempotent ingestion script will crash because tables already exist, or worse, append duplicate records into the analytical data warehouse. 

Build an **idempotent** ingestion script that processes staging records from `daily_ledger_staging`. The pipeline must:
1. Ensure table schema creation executes safely regardless of how many times the script is rerun (`CREATE TABLE IF NOT EXISTS`).
2. Guarantee that successive executions replace or update the staging partition cleanly rather than accumulating duplicate records.
3. Validate final table row counts and integrity.

### Data Schema Overview
- **`daily_ledger_staging` Table**: `entry_id` (INT), `account_code` (VARCHAR), `entry_date` (DATE), `amount` (DECIMAL)

### Objectives
1. Use idempotent SQL statements (`CREATE TABLE IF NOT EXISTS`, atomic replacement or upsert).
2. Test running the ingestion script twice in succession to prove idempotency.
3. Verify that the destination table contains the exact expected record count after both runs.

## Hints
- A pipeline is idempotent if $f(f(x)) = f(x)$—running it multiple times produces the exact same end state.
- In DuckDB / SQL, `CREATE OR REPLACE TABLE` or `CREATE TABLE IF NOT EXISTS` combined with partition clearing ensures idempotency.
""")

write_sol("sol3-8-medium-idempotent-table-creation.md", '''# Solution 3-8 (Medium): Building Idempotent Ingestion Pipelines

## Python & DuckDB Implementation
```python
import pandas as pd
import duckdb

raw_ledger = pd.DataFrame({
    'entry_id': [1001, 1002, 1003, 1004],
    'account_code': ['ACC-ASSET-01', 'ACC-LIAB-02', 'ACC-REV-03', 'ACC-EXP-04'],
    'entry_date': ['2024-03-01', '2024-03-01', '2024-03-01', '2024-03-01'],
    'amount': [1500.00, -500.00, 2800.00, -750.00]
})

def run_idempotent_pipeline(conn, df):
    # Reason: Register the input DataFrame
    conn.register('staging_feed', df)
    
    # Reason: 1. Idempotent DDL: CREATE TABLE IF NOT EXISTS avoids table collision errors
    conn.execute("""
        CREATE TABLE IF NOT EXISTS persistent_ledger (
            entry_id INT PRIMARY KEY,
            account_code VARCHAR(20),
            entry_date DATE,
            amount DECIMAL(10, 2)
        );
    """)
    
    # Reason: 2. Idempotent Ingestion: To avoid duplicate rows on re-runs,
    # delete overlapping partition dates before inserting fresh batch
    conn.execute("""
        DELETE FROM persistent_ledger 
        WHERE entry_date IN (SELECT DISTINCT CAST(entry_date AS DATE) FROM staging_feed);
    """)
    
    conn.execute("""
        INSERT INTO persistent_ledger
        SELECT entry_id, account_code, CAST(entry_date AS DATE), amount
        FROM staging_feed;
    """)
    
    count = conn.execute("SELECT COUNT(*) FROM persistent_ledger;").fetchone()[0]
    return count

conn = duckdb.connect(':memory:')

# Run 1
count_run_1 = run_idempotent_pipeline(conn, raw_ledger)
print(f"Run 1 completed. Total rows in persistent_ledger: {count_run_1}")

# Run 2 (Simulating pipeline retry)
count_run_2 = run_idempotent_pipeline(conn, raw_ledger)
print(f"Run 2 completed. Total rows in persistent_ledger: {count_run_2}")

assert count_run_1 == count_run_2 == len(raw_ledger), "Idempotency failed: Row count drifted!"
print("Idempotency verified: Pipeline executed multiple times with identical final state.")
conn.close()
```

## SQL Script Equivalent
```sql
-- Step 1: Safe table creation
CREATE TABLE IF NOT EXISTS persistent_ledger (
    entry_id INT PRIMARY KEY,
    account_code VARCHAR(20),
    entry_date DATE,
    amount DECIMAL(10, 2)
);

-- Step 2: Clear staging partition to avoid duplicate accumulation
DELETE FROM persistent_ledger 
WHERE entry_date = '2024-03-01';

-- Step 3: Insert verified data
INSERT INTO persistent_ledger (entry_id, account_code, entry_date, amount)
SELECT entry_id, account_code, CAST(entry_date AS DATE), amount
FROM staging_feed;
```
''')

# 3-9 Hard: Dirty ETL Pipeline DuckDB
write_act("act3-9-hard-dirty-etl-pipeline-duckdb.md", """# Activity 3-9 (Hard): End-to-End Messy Data ETL & Warehousing

## Problem Scenario
An enterprise retail chain ingests raw Point-of-Sale (POS) cash register logs into `raw_pos_transactions` and regional metadata into `store_dimension`. The POS raw logs are dirty:
1. `receipt_id` contains network duplicates that must be deduplicated.
2. `raw_store` has inconsistent casing (e.g. `'store-ca'`) and leading/trailing whitespace.
3. `raw_cashier` has irregular spaces and mixed case formatting.
4. `sale_amount` has `NULL` values from communication errors.
5. Some records reference invalid store codes that do not exist in `store_dimension`.

Build an end-to-end Python + SQL data engineering pipeline that:
1. **Pre-processes & Cleans**: Deduplicates receipts, trims and title-cases cashier names, trims and uppercases store codes.
2. **Imputes**: Imputes missing `sale_amount` with the median of valid sales.
3. **Relational Synthesis**: Performs an `INNER JOIN` with `store_dimension` (from Unit 1) to retrieve city and state tax rates.
4. **Calculates**: Computes `tax_amount = ROUND(sale_amount * tax_rate, 2)` and `total_collected = sale_amount + tax_amount`.
5. **Ingests**: Loads the clean dataset into a persistent local DuckDB analytical database table `clean_pos_sales`.

### Data Schema Overview
- **`raw_pos_transactions`**: `receipt_id` (VARCHAR), `raw_store` (VARCHAR), `raw_cashier` (VARCHAR), `sale_amount` (DECIMAL), `txn_date` (VARCHAR)
- **`store_dimension`**: `store_code` (VARCHAR), `city` (VARCHAR), `tax_rate` (DECIMAL)

### Objectives
1. Apply deduplication, string cleaning, and median imputation.
2. Join relational store dimensions.
3. Compute financial metrics.
4. Ingest into DuckDB.

## Hints
- Combine Pandas cleaning steps with DuckDB SQL queries or execute the entire pipeline inside Python before registering.
- Check row counts at each step to ensure unmapped stores or duplicates are handled according to business requirements.
""")

write_sol("sol3-9-hard-dirty-etl-pipeline-duckdb.md", '''# Solution 3-9 (Hard): End-to-End Messy Data ETL & Warehousing

## Python & DuckDB Production ETL Pipeline
```python
import pandas as pd
import numpy as np
import duckdb

raw_pos_transactions = pd.DataFrame({
    'receipt_id': ['RCP-001', 'RCP-001', 'RCP-002', 'RCP-003', 'RCP-004', 'RCP-005'],
    'raw_store': [' STORE-NY ', ' STORE-NY ', 'store-ca', 'STORE-TX', ' STORE-NY', 'STORE-UNKNOWN'],
    'raw_cashier': ['  JOHN DOE  ', '  JOHN DOE  ', 'alice smith', 'bob johnson', 'John Doe ', 'charlie'],
    'sale_amount': [150.00, 150.00, np.nan, 320.50, 95.00, 210.00],
    'txn_date': ['2024-02-01', '2024-02-01', '2024-02-01', '2024-02-02', '2024-02-02', '2024-02-03']
})

store_dimension = pd.DataFrame({
    'store_code': ['STORE-NY', 'STORE-CA', 'STORE-TX'],
    'city': ['New York', 'San Francisco', 'Austin'],
    'tax_rate': [0.088, 0.095, 0.082]
})

def run_pos_etl(db_path=":memory:"):
    df = raw_pos_transactions.copy()
    
    # Reason: 1. Deduplication - drop duplicate receipt IDs
    df = df.drop_duplicates(subset=['receipt_id'], keep='first').copy()
    
    # Reason: 2. String Standardization - clean store codes and cashier names
    df['store_code'] = df['raw_store'].apply(lambda x: str(x).strip().upper())
    df['cashier_name'] = df['raw_cashier'].apply(lambda x: str(x).strip().title())
    df['txn_date'] = pd.to_datetime(df['txn_date'])
    
    # Reason: 3. Median Imputation for missing numerical sales
    median_sale = df['sale_amount'].median()
    df['sale_amount'] = df['sale_amount'].fillna(median_sale)
    
    # Reason: 4. Relational Synthesis (Unit 1 Inner Join with store dimension)
    enriched_df = pd.merge(df, store_dimension, on='store_code', how='inner')
    
    # Reason: 5. Financial derived calculations
    enriched_df['tax_amount'] = (enriched_df['sale_amount'] * enriched_df['tax_rate']).round(2)
    enriched_df['total_collected'] = enriched_df['sale_amount'] + enriched_df['tax_amount']
    
    final_df = enriched_df[[
        'receipt_id', 'store_code', 'city', 'cashier_name', 
        'txn_date', 'sale_amount', 'tax_amount', 'total_collected'
    ]]
    
    # Reason: 6. DuckDB Ingestion
    conn = duckdb.connect(db_path)
    conn.register('virtual_clean_pos', final_df)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clean_pos_sales AS 
        SELECT * FROM virtual_clean_pos;
    """)
    
    warehouse_output = conn.execute("SELECT * FROM clean_pos_sales;").fetchdf()
    conn.close()
    return warehouse_output

result = run_pos_etl()
print("Final Ingested POS Sales in Warehouse:")
print(result)
```

## SQL Direct Imputation and Join Equivalent
```sql
WITH deduplicated_pos AS (
    SELECT 
        receipt_id,
        TRIM(UPPER(raw_store)) AS store_code,
        TRIM(raw_cashier) AS cashier_name,
        sale_amount,
        CAST(txn_date AS DATE) AS txn_date,
        ROW_NUMBER() OVER (PARTITION BY receipt_id ORDER BY txn_date ASC) AS rn
    FROM raw_pos_transactions
),
clean_pos AS (
    SELECT 
        receipt_id,
        store_code,
        cashier_name,
        COALESCE(sale_amount, 150.00) AS sale_amount,
        txn_date
    FROM deduplicated_pos
    WHERE rn = 1
)
SELECT 
    p.receipt_id,
    p.store_code,
    s.city,
    p.cashier_name,
    p.txn_date,
    p.sale_amount,
    ROUND(p.sale_amount * s.tax_rate, 2) AS tax_amount,
    p.sale_amount + ROUND(p.sale_amount * s.tax_rate, 2) AS total_collected
FROM clean_pos p
INNER JOIN store_dimension s ON p.store_code = s.store_code
ORDER BY p.txn_date ASC;
```
''')

# 3-10 Hard: Anomaly Audit Ingestion
write_act("act3-10-hard-anomaly-audit-ingestion.md", """# Activity 3-10 (Hard): Statistical Anomaly Quarantine & Warehouse Ingestion

## Problem Scenario
Industrial pressure readings from manufacturing equipment stream into `iot_factory_readings`. In real-world IoT environments, sensor failure modes manifest in two distinct ways: missing transmissions (`NULL`) and wild electrical anomalies (e.g. pressure spiking to nearly 200 PSI when baseline is 46 PSI). 

Synthesizing concepts across **all three units** (Unit 1 relational partitioning, Unit 2 windowed moving averages, and Unit 3 data quality & DuckDB ingestion), build an automated pipeline that:
1. Imputes missing pressure readings with the immediate 3-reading rolling moving average.
2. Computes the device-level rolling moving average using a sliding window.
3. Flags extreme anomalies where the actual pressure deviates from the moving average by more than 50% (`ABS(pressure - rolling_avg) / rolling_avg > 0.50`).
4. Splits the stream into two separate DuckDB tables:
   - **`factory_clean_telemetry`**: Clean, non-anomalous sensor readings.
   - **`telemetry_quarantine_audit`**: Anomalous records quarantined for engineering inspection.

### Data Schema Overview
- **`iot_factory_readings` Table**: `reading_id` (INT), `device_id` (VARCHAR), `reading_timestamp` (TIMESTAMP), `pressure_psi` (DECIMAL)

### Objectives
1. Compute rolling moving averages per device.
2. Detect statistical outlier anomalies.
3. Ingest split clean and quarantine tables into DuckDB.
4. Output summary verification of both tables.

## Hints
- Combine `.rolling()` or SQL window functions with conditional branching.
- Using DuckDB, you can run `CREATE TABLE clean_telemetry AS SELECT ... WHERE is_anomaly = FALSE` and `CREATE TABLE quarantine AS SELECT ... WHERE is_anomaly = TRUE`.
""")

write_sol("sol3-10-hard-anomaly-audit-ingestion.md", '''# Solution 3-10 (Hard): Statistical Anomaly Quarantine & Warehouse Ingestion

## Python & DuckDB Production Implementation
```python
import pandas as pd
import numpy as np
import duckdb

iot_readings = pd.DataFrame({
    'reading_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'device_id': ['PUMP-A', 'PUMP-A', 'PUMP-A', 'PUMP-A', 'PUMP-A', 'PUMP-A', 'PUMP-B', 'PUMP-B', 'PUMP-B', 'PUMP-B'],
    'reading_timestamp': [
        '2024-05-01 08:00:00', '2024-05-01 08:05:00', '2024-05-01 08:10:00',
        '2024-05-01 08:15:00', '2024-05-01 08:20:00', '2024-05-01 08:25:00',
        '2024-05-01 08:00:00', '2024-05-01 08:05:00', '2024-05-01 08:10:00', '2024-05-01 08:15:00'
    ],
    'pressure_psi': [45.2, 46.0, 45.8, 198.5, 46.1, 45.5, 60.1, 59.8, np.nan, 60.5]
})

iot_readings['reading_timestamp'] = pd.to_datetime(iot_readings['reading_timestamp'])
iot_readings = iot_readings.sort_values(by=['device_id', 'reading_timestamp']).reset_index(drop=True)

# Reason: 1. Impute missing sensor values with forward/backward fill or device median
iot_readings['pressure_psi'] = iot_readings.groupby('device_id')['pressure_psi'].transform(
    lambda group: group.fillna(group.median())
)

# Reason: 2. Compute 3-reading rolling moving average per device (Unit 2 Window Function)
iot_readings['rolling_avg_psi'] = (
    iot_readings.groupby('device_id')['pressure_psi']
    .rolling(window=3, min_periods=1)
    .mean()
    .round(2)
    .values
)

# Reason: 3. Anomaly detection: flag readings deviating > 50% from rolling baseline
iot_readings['anomaly_score'] = (
    np.abs(iot_readings['pressure_psi'] - iot_readings['rolling_avg_psi']) / iot_readings['rolling_avg_psi']
).round(3)

iot_readings['is_anomaly'] = iot_readings['anomaly_score'] > 0.50

# Reason: 4. DuckDB Ingestion and quarantine partitioning
conn = duckdb.connect(':memory:')
conn.register('virtual_telemetry', iot_readings)

# Ingest clean production telemetry
conn.execute("""
    CREATE TABLE factory_clean_telemetry AS 
    SELECT reading_id, device_id, reading_timestamp, pressure_psi, rolling_avg_psi
    FROM virtual_telemetry
    WHERE is_anomaly = FALSE;
""")

# Ingest quarantined audit telemetry
conn.execute("""
    CREATE TABLE telemetry_quarantine_audit AS 
    SELECT reading_id, device_id, reading_timestamp, pressure_psi, rolling_avg_psi, anomaly_score
    FROM virtual_telemetry
    WHERE is_anomaly = TRUE;
""")

clean_df = conn.execute("SELECT * FROM factory_clean_telemetry;").fetchdf()
quarantine_df = conn.execute("SELECT * FROM telemetry_quarantine_audit;").fetchdf()

print("Clean Telemetry Records:")
print(clean_df)
print("\nQuarantined Anomaly Records:")
print(quarantine_df)

conn.close()
```

## SQL Direct Implementation (DuckDB Dialect)
```sql
WITH windowed_telemetry AS (
    SELECT 
        reading_id,
        device_id,
        reading_timestamp,
        COALESCE(pressure_psi, MEDIAN(pressure_psi) OVER (PARTITION BY device_id)) AS pressure_psi,
        ROUND(AVG(pressure_psi) OVER (
            PARTITION BY device_id 
            ORDER BY reading_timestamp ASC 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 2) AS rolling_avg_psi
    FROM iot_factory_readings
),
anomaly_flagged AS (
    SELECT 
        *,
        ROUND(ABS(pressure_psi - rolling_avg_psi) / rolling_avg_psi, 3) AS anomaly_score,
        CASE 
            WHEN (ABS(pressure_psi - rolling_avg_psi) / rolling_avg_psi) > 0.50 THEN TRUE 
            ELSE FALSE 
        END AS is_anomaly
    FROM windowed_telemetry
)
-- Create Clean Production Table
CREATE TABLE factory_clean_telemetry AS 
SELECT reading_id, device_id, reading_timestamp, pressure_psi, rolling_avg_psi
FROM anomaly_flagged
WHERE is_anomaly = FALSE;

-- Create Quarantine Table
CREATE TABLE telemetry_quarantine_audit AS 
SELECT reading_id, device_id, reading_timestamp, pressure_psi, rolling_avg_psi, anomaly_score
FROM anomaly_flagged
WHERE is_anomaly = TRUE;
```
''')

print("Unit 3 generation complete.")
