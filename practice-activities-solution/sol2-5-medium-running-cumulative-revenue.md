# Solution 2-5 (Medium): Financial Running Total of Daily Revenue

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
