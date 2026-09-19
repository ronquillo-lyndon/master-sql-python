# Activity 2-6 (Medium): IoT Sensor Temperature Smoothing with Moving Average

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
