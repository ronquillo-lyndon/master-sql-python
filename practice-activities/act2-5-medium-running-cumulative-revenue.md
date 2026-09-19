# Activity 2-5 (Medium): Financial Running Total of Daily Revenue

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
