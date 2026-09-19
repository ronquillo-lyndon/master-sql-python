"""
Script to generate all 10 Unit 2 Activity and Solution markdown files.
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

print("Generating Unit 2 Activities and Solutions...")

# ==========================================
# UNIT 2
# ==========================================

# 2-1 Easy: Row Number Ranking
write_act("act2-1-easy-row-number-ranking.md", """# Activity 2-1 (Easy): Enumerating Transactions with ROW_NUMBER

## Problem Scenario
A risk operations team is auditing transaction histories in a `user_transactions` table. For account verification, fraud analysts need to label every transaction executed by each customer in strictly increasing sequential order (1st transaction, 2nd transaction, etc.) based on transaction timestamp. Unlike aggregate group-bys, each original transaction record must remain intact.

### Data Schema Overview
- **`user_transactions` Table**: `txn_id` (VARCHAR), `user_id` (INT), `txn_time` (TIMESTAMP), `amount` (DECIMAL)

### Objectives
1. Partition transactions by `user_id`.
2. Assign a continuous sequential integer starting at 1 for each user based on `txn_time` ascending.
3. Label the computed sequence column as `transaction_seq`.
4. Order the output by `user_id` ascending, then `transaction_seq` ascending.

## Hints
- `ROW_NUMBER()` is a window function evaluated across a partition without collapsing rows.
- The `PARTITION BY` sub-clause defines the boundary of unique users, while `ORDER BY` defines the sequence ordering.
- In Pandas, you can achieve this by grouping by `user_id` and calling `.cumcount() + 1`.
""")

write_sol("sol2-1-easy-row-number-ranking.md", """# Solution 2-1 (Easy): Enumerating Transactions with ROW_NUMBER

## SQL Implementation
```sql
SELECT 
    txn_id,
    user_id,
    txn_time,
    amount,
    -- Reason: ROW_NUMBER() assigns a unique ascending integer to each row within each user partition.
    -- PARTITION BY user_id resets the counter for each user.
    ROW_NUMBER() OVER (
        PARTITION BY user_id 
        ORDER BY txn_time ASC
    ) AS transaction_seq
FROM user_transactions
ORDER BY user_id ASC, transaction_seq ASC;
```

## Python Implementation
```python
import pandas as pd

user_transactions = pd.DataFrame({
    'txn_id': ['TXN-101', 'TXN-102', 'TXN-103', 'TXN-104', 'TXN-105', 'TXN-106'],
    'user_id': [1, 1, 1, 2, 2, 3],
    'txn_time': ['2024-01-01 08:30:00', '2024-01-02 09:15:00', '2024-01-05 14:20:00', '2024-01-01 11:00:00', '2024-01-03 16:45:00', '2024-01-02 10:10:00'],
    'amount': [45.00, 120.00, 60.00, 300.00, 85.00, 500.00]
})

user_transactions['txn_time'] = pd.to_datetime(user_transactions['txn_time'])

# Reason: Sort chronologically before assigning cumulative counts
df_sorted = user_transactions.sort_values(by=['user_id', 'txn_time']).reset_index(drop=True)

# Reason: .groupby('user_id').cumcount() generates 0-indexed ranking; adding 1 aligns with SQL 1-indexed ROW_NUMBER
df_sorted['transaction_seq'] = df_sorted.groupby('user_id').cumcount() + 1

print(df_sorted)
```
""")

# 2-2 Easy: Dense Rank Leaderboard
write_act("act2-2-easy-dense-rank-leaderboard.md", """# Activity 2-2 (Easy): Regional Sales Leaderboard with DENSE_RANK

## Problem Scenario
The VP of Sales needs a performance leaderboard for sales representatives stored in `sales_reps`. Reps are evaluated by `closed_revenue` within their designated sales `region`. If two or more reps achieve the exact same revenue, they must share the same rank, and the subsequent rank must be assigned consecutively without skipping any integer rank numbers (e.g., ranks 1, 1, 2 rather than 1, 1, 3).

### Data Schema Overview
- **`sales_reps` Table**: `rep_id` (INT), `rep_name` (VARCHAR), `region` (VARCHAR), `closed_revenue` (DECIMAL)

### Objectives
1. Partition the rankings by `region`.
2. Rank sales representatives based on `closed_revenue` in descending order.
3. Use dense ranking so ties do not create gaps in the rank sequence.
4. Order the output by `region` ascending, then `regional_rank` ascending.

## Hints
- Standard `RANK()` skips rank integers after a tie, while `DENSE_RANK()` guarantees contiguous integers.
- In Pandas, the `.rank()` method accepts a `method` parameter. Review the differences between `'average'`, `'min'`, and `'dense'`.
""")

write_sol("sol2-2-easy-dense-rank-leaderboard.md", """# Solution 2-2 (Easy): Regional Sales Leaderboard with DENSE_RANK

## SQL Implementation
```sql
SELECT 
    rep_id,
    rep_name,
    region,
    closed_revenue,
    -- Reason: DENSE_RANK() assigns consecutive ranks for ties without gaps (e.g. 1, 1, 2)
    DENSE_RANK() OVER (
        PARTITION BY region 
        ORDER BY closed_revenue DESC
    ) AS regional_rank
FROM sales_reps
ORDER BY region ASC, regional_rank ASC;
```

## Python Implementation
```python
import pandas as pd

sales_reps = pd.DataFrame({
    'rep_id': [1, 2, 3, 4, 5, 6, 7],
    'rep_name': ['Alice Walker', 'Bob Stone', 'Charlie Hayes', 'Diana Prince', 'Evan Wright', 'Fiona Gallagher', 'George Clark'],
    'region': ['North', 'North', 'North', 'North', 'South', 'South', 'South'],
    'closed_revenue': [150000.00, 120000.00, 150000.00, 95000.00, 180000.00, 180000.00, 130000.00]
})

# Reason: Replicate SQL DENSE_RANK partitioned by region
# method='dense' ensures consecutive rank integers upon ties; ascending=False ranks highest revenue first
sales_reps['regional_rank'] = (
    sales_reps.groupby('region')['closed_revenue']
    .rank(method='dense', ascending=False)
    .astype(int)
)

# Reason: Sort results to match presentation requirements
result_df = sales_reps.sort_values(by=['region', 'regional_rank']).reset_index(drop=True)
print(result_df)
```
""")

# 2-3 Easy: Lag Period Comparison
write_act("act2-3-easy-lag-period-comparison.md", """# Activity 2-3 (Easy): Day-over-Day Server Ingestion Delta with LAG

## Problem Scenario
Site Reliability Engineers (SRE) monitor API traffic recorded in `server_metrics`. To detect sudden traffic spikes or throughput drops, the engineering lead needs a daily report comparing current day `request_count` against the previous day's `request_count`. The report must compute the day-over-day delta (`current - previous`). For the very first recorded day, the delta should fall back to 0.

### Data Schema Overview
- **`server_metrics` Table**: `metric_date` (DATE), `request_count` (INT), `error_count` (INT)

### Objectives
1. Retrieve the prior day's request volume using the `LAG` window function.
2. Calculate `day_over_day_delta` (`request_count - prev_request_count`).
3. For the initial day with no predecessor, ensure `day_over_day_delta` defaults to `0`.
4. Order the output chronologically by `metric_date`.

## Hints
- `LAG(column, offset, default_value)` accesses previous row values without performing a self-join.
- In Pandas, the `.shift()` method shifts Series values along the index; shifting by positive 1 pulls the prior row's value down.
""")

write_sol("sol2-3-easy-lag-period-comparison.md", """# Solution 2-3 (Easy): Day-over-Day Server Ingestion Delta with LAG

## SQL Implementation
```sql
SELECT 
    metric_date,
    request_count,
    -- Reason: LAG(..., 1, request_count) retrieves the preceding row's request_count.
    -- Supplying request_count as third argument defaults the first row's prior value to itself, resulting in a 0 delta.
    LAG(request_count, 1, request_count) OVER (
        ORDER BY metric_date ASC
    ) AS prev_request_count,
    -- Reason: Compute the delta between current day and prior day
    request_count - LAG(request_count, 1, request_count) OVER (
        ORDER BY metric_date ASC
    ) AS day_over_day_delta
FROM server_metrics
ORDER BY metric_date ASC;
```

## Python Implementation
```python
import pandas as pd

server_metrics = pd.DataFrame({
    'metric_date': ['2024-03-01', '2024-03-02', '2024-03-03', '2024-03-04', '2024-03-05', '2024-03-06', '2024-03-07'],
    'request_count': [12000, 14500, 13800, 18200, 21000, 19500, 22500],
    'error_count': [45, 52, 39, 110, 140, 95, 105]
})

server_metrics['metric_date'] = pd.to_datetime(server_metrics['metric_date'])
server_metrics = server_metrics.sort_values(by='metric_date').reset_index(drop=True)

# Reason: .shift(1) accesses preceding row equivalent to SQL LAG(..., 1)
server_metrics['prev_request_count'] = server_metrics['request_count'].shift(1)

# Reason: For the initial row where shift produces NaN, fill with the current request_count to make delta 0
server_metrics['prev_request_count'] = server_metrics['prev_request_count'].fillna(server_metrics['request_count']).astype(int)

# Reason: Vectorized calculation of day-over-day difference
server_metrics['day_over_day_delta'] = server_metrics['request_count'] - server_metrics['prev_request_count']

print(server_metrics[['metric_date', 'request_count', 'prev_request_count', 'day_over_day_delta']])
```
""")

# 2-4 Easy: Lead Forward Tracking
write_act("act2-4-easy-lead-forward-tracking.md", """# Activity 2-4 (Easy): Tracking Next User Action with LEAD

## Problem Scenario
A product analytics team is studying web conversion funnels recorded in a `user_events` table. To understand navigational flow within each user session (`session_id`), the team needs to know the subsequent page visited (`next_page`) and the timestamp of that subsequent event. If the event is the terminal action of the session, `next_page` should display `'SESSION_END'`.

### Data Schema Overview
- **`user_events` Table**: `event_id` (INT), `session_id` (VARCHAR), `event_time` (TIMESTAMP), `page_name` (VARCHAR)

### Objectives
1. Partition the events by `session_id`.
2. Order events chronologically by `event_time`.
3. Use `LEAD` to project the next visited `page_name`.
4. Replace NULL in terminal events with `'SESSION_END'`.
5. Order output by `session_id`, then `event_time`.

## Hints
- `LEAD` looks forward into future rows within the defined window frame.
- Specify a default fallback value in `LEAD` to handle the final row in each partition gracefully.
- In Pandas, `.shift(-1)` shifts rows upward to look forward into the subsequent record.
""")

write_sol("sol2-4-easy-lead-forward-tracking.md", """# Solution 2-4 (Easy): Tracking Next User Action with LEAD

## SQL Implementation
```sql
SELECT 
    event_id,
    session_id,
    event_time,
    page_name AS current_page,
    -- Reason: LEAD looks ahead 1 row within each session. Default value 'SESSION_END' handles the last event.
    LEAD(page_name, 1, 'SESSION_END') OVER (
        PARTITION BY session_id 
        ORDER BY event_time ASC
    ) AS next_page
FROM user_events
ORDER BY session_id ASC, event_time ASC;
```

## Python Implementation
```python
import pandas as pd

user_events = pd.DataFrame({
    'event_id': [1, 2, 3, 4, 5, 6, 7],
    'session_id': ['SESS-A', 'SESS-A', 'SESS-A', 'SESS-A', 'SESS-B', 'SESS-B', 'SESS-B'],
    'event_time': ['2024-03-10 10:00:00', '2024-03-10 10:02:15', '2024-03-10 10:06:40', '2024-03-10 10:08:10', '2024-03-10 11:15:00', '2024-03-10 11:17:30', '2024-03-10 11:19:00'],
    'page_name': ['homepage', 'product_catalog', 'product_detail', 'cart', 'landing_page', 'signup_form', 'dashboard']
})

user_events['event_time'] = pd.to_datetime(user_events['event_time'])
user_events = user_events.sort_values(by=['session_id', 'event_time']).reset_index(drop=True)

# Reason: Replicate SQL LEAD using .groupby('session_id')['page_name'].shift(-1)
user_events['next_page'] = user_events.groupby('session_id')['page_name'].shift(-1)

# Reason: Fill missing trailing event with designated literal string
user_events['next_page'] = user_events['next_page'].fillna('SESSION_END')

print(user_events[['session_id', 'event_time', 'page_name', 'next_page']])
```
""")

# 2-5 Medium: Running Cumulative Revenue
write_act("act2-5-medium-running-cumulative-revenue.md", """# Activity 2-5 (Medium): Financial Running Total of Daily Revenue

## Problem Scenario
A SaaS company monitors financial trajectory in a `daily_financials` table. The CFO wants a cumulative revenue curve starting from the first day of the year through each consecutive date. The analytics pipeline must calculate the running total of `daily_revenue` alongside the cumulative number of new subscribers acquired.

### Data Schema Overview
- **`daily_financials` Table**: `record_date` (DATE), `new_subscribers` (INT), `daily_revenue` (DECIMAL)

### Objectives
1. Order records strictly chronologically by `record_date`.
2. Compute `running_cumulative_revenue` using an unbounded preceding window frame.
3. Compute `running_cumulative_subscribers` using an unbounded preceding window frame.
4. Output `record_date`, `daily_revenue`, `running_cumulative_revenue`, `new_subscribers`, and `running_cumulative_subscribers`.

## Hints
- A window specification with `ORDER BY column ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` accumulates all prior records up to the active row.
- In Pandas, cumulative aggregations are performed efficiently using the vectorized `.cumsum()` method.
""")

write_sol("sol2-5-medium-running-cumulative-revenue.md", """# Solution 2-5 (Medium): Financial Running Total of Daily Revenue

## SQL Implementation
```sql
SELECT 
    record_date,
    daily_revenue,
    -- Reason: Compute running cumulative revenue from beginning of data stream to current row
    SUM(daily_revenue) OVER (
        ORDER BY record_date ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_cumulative_revenue,
    new_subscribers,
    -- Reason: Compute cumulative subscriber acquisitions
    SUM(new_subscribers) OVER (
        ORDER BY record_date ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_cumulative_subscribers
FROM daily_financials
ORDER BY record_date ASC;
```

## Python Implementation
```python
import pandas as pd

daily_financials = pd.DataFrame({
    'record_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-06', '2024-01-07', '2024-01-08'],
    'new_subscribers': [12, 18, 15, 22, 30, 25, 28, 35],
    'daily_revenue': [1200.00, 1850.00, 1400.00, 2300.00, 3100.00, 2750.00, 2900.00, 3800.00]
})

daily_financials['record_date'] = pd.to_datetime(daily_financials['record_date'])
daily_financials = daily_financials.sort_values(by='record_date').reset_index(drop=True)

# Reason: Replicate SQL UNBOUNDED PRECEDING window sum using vectorized .cumsum()
daily_financials['running_cumulative_revenue'] = daily_financials['daily_revenue'].cumsum()
daily_financials['running_cumulative_subscribers'] = daily_financials['new_subscribers'].cumsum()

print(daily_financials)
```
""")

# 2-6 Medium: Rolling Moving Average
write_act("act2-6-medium-rolling-moving-average.md", """# Activity 2-6 (Medium): IoT Sensor Temperature Smoothing with Moving Average

## Problem Scenario
An industrial IoT temperature monitoring system logs environmental readings in `sensor_telemetry`. Raw readings often exhibit momentary spikes caused by intermittent electrical noise. To provide stable inputs for predictive maintenance models, the data engineering pipeline must calculate a 3-day sliding moving average of `temperature_celsius` per sensor, rounded to two decimal places.

### Data Schema Overview
- **`sensor_telemetry` Table**: `reading_id` (INT), `sensor_id` (VARCHAR), `reading_day` (DATE), `temperature_celsius` (DECIMAL)

### Objectives
1. Partition window calculations by `sensor_id`.
2. Order readings chronologically by `reading_day`.
3. Compute a 3-day sliding average covering the current day and up to 2 preceding days (`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`).
4. Round the moving average to two decimal places (`three_day_avg_temp`).
5. Order output by `sensor_id`, then `reading_day`.

## Hints
- The window frame specification `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` ensures that exactly 3 physical rows are included in the average (or fewer if at the beginning of the partition).
- In Pandas, combine `.groupby('sensor_id')` with `.rolling(window=3, min_periods=1).mean()`.
""")

write_sol("sol2-6-medium-rolling-moving-average.md", """# Solution 2-6 (Medium): IoT Sensor Temperature Smoothing with Moving Average

## SQL Implementation
```sql
SELECT 
    reading_id,
    sensor_id,
    reading_day,
    temperature_celsius,
    -- Reason: Compute moving average across current day and preceding 2 days (3-day rolling window)
    ROUND(AVG(temperature_celsius) OVER (
        PARTITION BY sensor_id
        ORDER BY reading_day ASC
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS three_day_avg_temp
FROM sensor_telemetry
ORDER BY sensor_id ASC, reading_day ASC;
```

## Python Implementation
```python
import pandas as pd

sensor_telemetry = pd.DataFrame({
    'reading_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'sensor_id': ['SENSOR-01'] * 10,
    'reading_day': ['2024-04-01', '2024-04-02', '2024-04-03', '2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09', '2024-04-10'],
    'temperature_celsius': [22.50, 23.10, 25.40, 24.80, 28.20, 29.00, 26.50, 23.00, 22.80, 21.90]
})

sensor_telemetry['reading_day'] = pd.to_datetime(sensor_telemetry['reading_day'])
sensor_telemetry = sensor_telemetry.sort_values(by=['sensor_id', 'reading_day']).reset_index(drop=True)

# Reason: Replicate SQL sliding window average using Pandas .rolling()
# min_periods=1 ensures initial rows calculate the average of available days rather than returning NaN
sensor_telemetry['three_day_avg_temp'] = (
    sensor_telemetry.groupby('sensor_id')['temperature_celsius']
    .rolling(window=3, min_periods=1)
    .mean()
    .round(2)
    .values
)

print(sensor_telemetry)
```
""")

# 2-7 Medium: Partitioned Window Stats
write_act("act2-7-medium-partitioned-window-stats.md", """# Activity 2-7 (Medium): Departmental Salary Differential Analysis

## Problem Scenario
The compensation committee tracks staff pay in `employee_compensation`. Management wants to evaluate internal equity by comparing each employee's individual base salary directly against their departmental average. For each employee, display their department name, individual salary, the department's average salary, and the salary difference (`base_salary - dept_avg_salary`). The query must not collapse individual employee rows.

### Data Schema Overview
- **`employee_compensation` Table**: `emp_id` (INT), `name` (VARCHAR), `dept_name` (VARCHAR), `base_salary` (DECIMAL)

### Objectives
1. Compute the department average salary using an unconstrained window partition (`OVER (PARTITION BY dept_name)`).
2. Calculate the salary difference between the employee's salary and their department average.
3. Round monetary figures to two decimal places.
4. Order the output by `dept_name` ascending, then `base_salary` descending.

## Hints
- Omitting `ORDER BY` and frame clauses in an `OVER (PARTITION BY ...)` specification calculates the aggregate across the entire partition without sliding.
- In Pandas, this operation is accomplished using `.groupby('dept_name')['base_salary'].transform('mean')`, which broadcasts the group mean back to the original DataFrame rows.
""")

write_sol("sol2-7-medium-partitioned-window-stats.md", """# Solution 2-7 (Medium): Departmental Salary Differential Analysis

## SQL Implementation
```sql
SELECT 
    emp_id,
    name,
    dept_name,
    base_salary,
    -- Reason: Compute full departmental average across all members of the partition without row collapse
    ROUND(AVG(base_salary) OVER (
        PARTITION BY dept_name
    ), 2) AS dept_avg_salary,
    -- Reason: Calculate the differential against the departmental baseline
    ROUND(base_salary - AVG(base_salary) OVER (
        PARTITION BY dept_name
    ), 2) AS salary_diff_from_avg
FROM employee_compensation
ORDER BY dept_name ASC, base_salary DESC;
```

## Python Implementation
```python
import pandas as pd

employee_compensation = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'name': ['Alice Cooper', 'Bob Martin', 'Charlie Daniels', 'Diana Ross', 'Edward Norton', 'Fiona Apple', 'Gordon Ramsay', 'Hannah Abbott'],
    'dept_name': ['Engineering', 'Engineering', 'Engineering', 'Finance', 'Finance', 'Marketing', 'Marketing', 'Marketing'],
    'base_salary': [130000.00, 110000.00, 150000.00, 95000.00, 105000.00, 88000.00, 92000.00, 115000.00]
})

# Reason: Replicate SQL PARTITION BY aggregate broadcast using .transform('mean')
# .transform preserves original row dimensions
employee_compensation['dept_avg_salary'] = (
    employee_compensation.groupby('dept_name')['base_salary']
    .transform('mean')
    .round(2)
)

# Reason: Vectorized calculation of salary disparity
employee_compensation['salary_diff_from_avg'] = (
    employee_compensation['base_salary'] - employee_compensation['dept_avg_salary']
).round(2)

result_df = employee_compensation.sort_values(by=['dept_name', 'base_salary'], ascending=[True, False])
print(result_df)
```
""")

# 2-8 Medium: CTE Sequential Pipeline
write_act("act2-8-medium-cte-sequential-pipeline.md", """# Activity 2-8 (Medium): Multi-Step Funnel with Common Table Expressions (CTEs)

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
""")

write_sol("sol2-8-medium-cte-sequential-pipeline.md", """# Solution 2-8 (Medium): Multi-Step Funnel with Common Table Expressions (CTEs)

## SQL Implementation
```sql
-- Step 1: Aggregate high-frequency orders to daily store grain
WITH daily_store_sales_cte AS (
    SELECT 
        CAST(order_timestamp AS DATE) AS sale_date,
        store_id,
        SUM(order_value) AS daily_revenue
    FROM store_orders
    GROUP BY CAST(order_timestamp AS DATE), store_id
),
-- Step 2: Rank stores per day based on gross daily revenue
ranked_stores_cte AS (
    SELECT 
        sale_date,
        store_id,
        daily_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY sale_date 
            ORDER BY daily_revenue DESC
        ) AS daily_rank
    FROM daily_store_sales_cte
)
-- Step 3: Extract the winning store for each date
SELECT 
    sale_date,
    store_id AS top_store_id,
    daily_revenue AS top_store_revenue
FROM ranked_stores_cte
WHERE daily_rank = 1
ORDER BY sale_date ASC;
```

## Python Implementation
```python
import pandas as pd

store_orders = pd.DataFrame({
    'order_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'store_id': [101, 101, 101, 102, 102, 102, 103, 103],
    'order_timestamp': ['2024-02-01 10:15:00', '2024-02-01 14:20:00', '2024-02-02 09:30:00', '2024-02-01 11:00:00', '2024-02-02 16:00:00', '2024-02-02 18:30:00', '2024-02-01 08:45:00', '2024-02-02 12:10:00'],
    'order_value': [45.00, 120.00, 310.00, 80.00, 520.00, 140.00, 950.00, 400.00]
})

store_orders['order_date'] = pd.to_datetime(store_orders['order_timestamp']).dt.date

# Reason: Replicate Step 1 CTE - Group by date and store
daily_store_sales = store_orders.groupby(['order_date', 'store_id'])['order_value'].sum().reset_index(name='daily_revenue')

# Reason: Replicate Step 2 CTE - Rank stores within each date
daily_store_sales['daily_rank'] = (
    daily_store_sales.groupby('order_date')['daily_revenue']
    .rank(method='first', ascending=False)
    .astype(int)
)

# Reason: Replicate Step 3 Final Query - Filter for top rank and sort
top_stores = daily_store_sales[daily_store_sales['daily_rank'] == 1].sort_values(by='order_date').reset_index(drop=True)
top_stores = top_stores.rename(columns={'store_id': 'top_store_id', 'daily_revenue': 'top_store_revenue'})

print(top_stores[['order_date', 'top_store_id', 'top_store_revenue']])
```
""")

# 2-9 Hard: Weighted Moving Avg SymPy
write_act("act2-9-hard-weighted-moving-avg-sympy.md", """# Activity 2-9 (Hard): Symbolic Formula Derivation & Weighted Moving Average

## Problem Scenario
A quantitative trading desk analyses daily equity closing prices recorded in `stock_price_history`. Quantitative analysts want to smooth price volatility using a 3-day exponentially decaying weighted moving average where:
- Day $t$ (today) receives weight $w_3 = 0.5$
- Day $t-1$ (yesterday) receives weight $w_2 = 0.3$
- Day $t-2$ (two days ago) receives weight $w_1 = 0.2$

The analytical engineering workflow requires:
1. **Symbolic Derivation**: Use SymPy to algebraically formulate the weighted average equation, simplify it, and verify that the weights sum to 1.0.
2. **SQL & Programmatic Implementation**: Use analytical window functions (`LAG`) in SQL and vectorized `.shift()` in Pandas to calculate the weighted moving average across the time series. For the first two trading dates (where 3 full days of history do not exist), output `NULL` or `NaN`.

### Data Schema Overview
- **`stock_price_history` Table**: `trade_date` (DATE), `ticker` (VARCHAR), `close_price` (DECIMAL)

### Objectives
1. Define algebraic symbols in SymPy and substitute weight values.
2. Implement lag window functions to extract historical prices at offsets 1 and 2.
3. Compute `weighted_moving_avg = (0.5 * close_price) + (0.3 * lag1) + (0.2 * lag2)`.
4. Order output by `trade_date` ascending.

## Hints
- In SymPy, define symbols with `sp.symbols('p0 p1 p2 w1 w2 w3')` and compute the weighted expression divided by the sum of weights.
- In SQL, `LAG(close_price, 1)` and `LAG(close_price, 2)` retrieve prior day values. A `CASE WHEN` can suppress rows without 2 preceding trading days.
""")

write_sol("sol2-9-hard-weighted-moving-avg-sympy.md", """# Solution 2-9 (Hard): Symbolic Formula Derivation & Weighted Moving Average

## Python Implementation (SymPy Derivation + Vectorized Pandas)
```python
import sympy as sp
import pandas as pd
import numpy as np

# ==========================================
# 1. SymPy Step: Symbolic Formula Verification
# ==========================================
# Reason: Algebraically verify weight distribution before deploying to pipeline
p0, p1, p2 = sp.symbols('p0 p1 p2') # p0 = current, p1 = lag1, p2 = lag2
w0, w1, w2 = sp.symbols('w0 w1 w2')

formula = (p0 * w0 + p1 * w1 + p2 * w2) / (w0 + w1 + w2)
verified_formula = formula.subs({w0: 0.5, w1: 0.3, w2: 0.2})
print(f"Verified Symbolic Formula: {verified_formula}")

# ==========================================
# 2. Vectorized Pandas Execution
# ==========================================
stock_price_history = pd.DataFrame({
    'trade_date': ['2024-03-01', '2024-03-04', '2024-03-05', '2024-03-06', '2024-03-07', '2024-03-08', '2024-03-11', '2024-03-12'],
    'ticker': ['ACME'] * 8,
    'close_price': [100.00, 105.00, 102.50, 110.00, 108.00, 115.00, 118.50, 114.00]
})

stock_price_history['trade_date'] = pd.to_datetime(stock_price_history['trade_date'])
stock_price_history = stock_price_history.sort_values(by='trade_date').reset_index(drop=True)

# Reason: Use .shift() to obtain lag1 and lag2
stock_price_history['lag1'] = stock_price_history['close_price'].shift(1)
stock_price_history['lag2'] = stock_price_history['close_price'].shift(2)

# Reason: Implement symbolically verified formula
stock_price_history['weighted_moving_avg'] = (
    0.5 * stock_price_history['close_price'] + 
    0.3 * stock_price_history['lag1'] + 
    0.2 * stock_price_history['lag2']
).round(2)

print(stock_price_history[['trade_date', 'ticker', 'close_price', 'weighted_moving_avg']])
```

## SQL Implementation
```sql
WITH lagged_prices AS (
    SELECT 
        trade_date,
        ticker,
        close_price,
        -- Reason: LAG accesses prior prices at offset 1 and offset 2
        LAG(close_price, 1) OVER (ORDER BY trade_date ASC) AS lag1,
        LAG(close_price, 2) OVER (ORDER BY trade_date ASC) AS lag2
    FROM stock_price_history
)
SELECT 
    trade_date,
    ticker,
    close_price,
    -- Reason: If lag2 is NULL, less than 3 days of historical data exist; return NULL
    CASE 
        WHEN lag2 IS NOT NULL THEN 
            ROUND((0.5 * close_price) + (0.3 * lag1) + (0.2 * lag2), 2)
        ELSE NULL 
    END AS weighted_moving_avg
FROM lagged_prices
ORDER BY trade_date ASC;
```
""")

# 2-10 Hard: Retention Cohort Progression
write_act("act2-10-hard-retention-cohort-progression.md", """# Activity 2-10 (Hard): Customer Retention & Purchase Interval Pipeline

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
""")

write_sol("sol2-10-hard-retention-cohort-progression.md", """# Solution 2-10 (Hard): Customer Retention & Purchase Interval Pipeline

## SQL Implementation
```sql
WITH customer_order_stream AS (
    SELECT 
        s.customer_id,
        s.signup_date,
        s.channel,
        p.purchase_id,
        p.purchase_date,
        p.amount,
        -- Reason: Assign order sequence for each customer; NULL for non-purchasing customers
        CASE 
            WHEN p.purchase_id IS NOT NULL THEN 
                ROW_NUMBER() OVER (PARTITION BY s.customer_id ORDER BY p.purchase_date ASC)
            ELSE 0 
        END AS order_seq,
        -- Reason: Retrieve previous purchase date for the customer
        LAG(p.purchase_date, 1) OVER (PARTITION BY s.customer_id ORDER BY p.purchase_date ASC) AS prior_purchase_date
    FROM customer_signups s
    -- Reason: LEFT JOIN preserves non-purchasing customers like customer 4
    LEFT JOIN customer_purchases p 
        ON s.customer_id = p.customer_id
)
SELECT 
    customer_id,
    channel,
    signup_date,
    purchase_id,
    purchase_date,
    COALESCE(amount, 0.00) AS amount,
    order_seq,
    -- Reason: Calculate day interval since prior purchase; 0 for first order or non-purchasers
    CASE 
        WHEN prior_purchase_date IS NOT NULL THEN (CAST(purchase_date AS DATE) - CAST(prior_purchase_date AS DATE))
        ELSE 0 
    END AS days_since_prior_purchase
FROM customer_order_stream
ORDER BY customer_id ASC, order_seq ASC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

customer_signups = pd.DataFrame({
    'customer_id': [1, 2, 3, 4],
    'signup_date': ['2024-01-01', '2024-01-02', '2024-01-05', '2024-01-10'],
    'channel': ['Organic', 'Paid Search', 'Referral', 'Organic']
})

customer_purchases = pd.DataFrame({
    'purchase_id': [101, 102, 103, 104, 105, 106],
    'customer_id': [1, 1, 1, 2, 2, 3],
    'purchase_date': ['2024-01-03', '2024-01-20', '2024-02-15', '2024-01-04', '2024-01-05', '2024-01-12'],
    'amount': [50.00, 80.00, 120.00, 300.00, 150.00, 45.00]
})

# Reason: Step 1 - Relational LEFT JOIN to preserve inactive signups
merged_df = pd.merge(customer_signups, customer_purchases, on='customer_id', how='left')

# Convert dates to datetime
merged_df['purchase_date'] = pd.to_datetime(merged_df['purchase_date'])
merged_df['signup_date'] = pd.to_datetime(merged_df['signup_date'])
merged_df = merged_df.sort_values(by=['customer_id', 'purchase_date']).reset_index(drop=True)

# Reason: Step 2 - Compute order sequence per customer (0 for non-purchasers)
merged_df['order_seq'] = np.where(
    merged_df['purchase_id'].notna(),
    merged_df.groupby('customer_id').cumcount() + 1,
    0
)

# Reason: Step 3 - Shift purchase date to get prior purchase date
merged_df['prior_purchase_date'] = merged_df.groupby('customer_id')['purchase_date'].shift(1)

# Reason: Step 4 - Calculate days difference; fill NaN with 0
day_diff = (merged_df['purchase_date'] - merged_df['prior_purchase_date']).dt.days
merged_df['days_since_prior_purchase'] = day_diff.fillna(0).astype(int)

# Reason: Resolve unpurchased amounts
merged_df['amount'] = merged_df['amount'].fillna(0.00)

print(merged_df[['customer_id', 'channel', 'purchase_id', 'purchase_date', 'amount', 'order_seq', 'days_since_prior_purchase']])
```
""")

print("Unit 2 generation complete.")
