# Activity 3-10 (Hard): Statistical Anomaly Quarantine & Warehouse Ingestion

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
