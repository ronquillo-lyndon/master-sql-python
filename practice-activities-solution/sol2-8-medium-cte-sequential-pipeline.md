# Solution 2-8 (Medium): Multi-Step Funnel with Common Table Expressions (CTEs)

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
