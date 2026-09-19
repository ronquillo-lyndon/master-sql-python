# Solution 3-10 (Hard): Statistical Anomaly Quarantine & Warehouse Ingestion

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
print("
Quarantined Anomaly Records:")
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
