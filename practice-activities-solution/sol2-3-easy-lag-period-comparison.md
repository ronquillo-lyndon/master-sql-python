# Solution 2-3 (Easy): Day-over-Day Server Ingestion Delta with LAG

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
