# Solution 2-6 (Medium): IoT Sensor Temperature Smoothing with Moving Average

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
