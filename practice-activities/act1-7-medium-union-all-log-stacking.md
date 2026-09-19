# Activity 1-7 (Medium): Unifying Web and Mobile Event Streams

## Problem Scenario
A product analytics team monitors engagement across two independent channels: desktop web sessions stored in `web_clicks` and native smartphone interactions stored in `mobile_taps`. To run cross-platform user journey analyses, the data engineering team needs to stack these two event streams into a single unified event timeline. The resulting dataset must normalize column names, add a source platform flag (`'WEB'` vs `'MOBILE'`), and present all interactions chronologically.

### Data Schema Overview
- **`web_clicks` Table**: `event_id` (VARCHAR), `user_id` (INT), `action_type` (VARCHAR), `event_timestamp` (VARCHAR)
- **`mobile_taps` Table**: `event_id` (VARCHAR), `user_id` (INT), `action_type` (VARCHAR), `event_timestamp` (VARCHAR)

### Objectives
1. Combine records from both tables without discarding duplicate user actions using set stacking (`UNION ALL`).
2. Add a literal discriminator column `platform` (`'WEB'` or `'MOBILE'`).
3. Output `event_id`, `user_id`, `platform`, `action_type`, and `event_timestamp`.
4. Order by `event_timestamp` ascending.

## Hints
- `UNION ALL` stacks rows from multiple result sets without the performance overhead of deduplicating records.
- In Pandas, vertical concatenation is achieved using `pd.concat()`, passing an array of DataFrames with matching schema columns.
