# Activity 2-2 (Easy): Regional Sales Leaderboard with DENSE_RANK

## Problem Scenario
The VP of Sales needs a performance leaderboard for sales representatives stored in `sales_reps`. Reps are evaluated by `closed_revenue` within their designated sales `region`. If two or more reps achieve the exact same revenue, they must share the same rank, and the subsequent rank must be assigned consecutively without skipping any integer rank numbers (e.g., ranks 1, 1, 2 rather than 1, 1, 3).

### Data Schema Overview
- **`sales_reps` Table**: `rep_id` (INT), `rep_name` (VARCHAR), `region` (VARCHAR), `closed_revenue` (DECIMAL)

### Objectives
1. Partition the rankings by `region`.
2. Rank sales representatives based on `closed_revenue` in descending order.
3. Use dense ranking so ties do not create gaps in the rank sequence.
4. Order the output by `region` ascending, then `regional_rank` ascending.

## Hints
- Standard `RANK()` skips rank integers after a tie, while `DENSE_RANK()` guarantees contiguous integers.
- In Pandas, the `.rank()` method accepts a `method` parameter. Review the differences between `'average'`, `'min'`, and `'dense'`.
