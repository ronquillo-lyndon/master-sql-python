# Activity 2-1 (Easy): Enumerating Transactions with ROW_NUMBER

## Problem Scenario
A risk operations team is auditing transaction histories in a `user_transactions` table. For account verification, fraud analysts need to label every transaction executed by each customer in strictly increasing sequential order (1st transaction, 2nd transaction, etc.) based on transaction timestamp. Unlike aggregate group-bys, each original transaction record must remain intact.

### Data Schema Overview
- **`user_transactions` Table**: `txn_id` (VARCHAR), `user_id` (INT), `txn_time` (TIMESTAMP), `amount` (DECIMAL)

### Objectives
1. Partition transactions by `user_id`.
2. Assign a continuous sequential integer starting at 1 for each user based on `txn_time` ascending.
3. Label the computed sequence column as `transaction_seq`.
4. Order the output by `user_id` ascending, then `transaction_seq` ascending.

## Hints
- `ROW_NUMBER()` is a window function evaluated across a partition without collapsing rows.
- The `PARTITION BY` sub-clause defines the boundary of unique users, while `ORDER BY` defines the sequence ordering.
- In Pandas, you can achieve this by grouping by `user_id` and calling `.cumcount() + 1`.
