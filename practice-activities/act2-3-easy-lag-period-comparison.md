# Activity 2-3 (Easy): Day-over-Day Server Ingestion Delta with LAG

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
