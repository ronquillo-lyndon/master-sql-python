# Solution 2-1 (Easy): Enumerating Transactions with ROW_NUMBER

## SQL Implementation
```sql
SELECT 
    txn_id,
    user_id,
    txn_time,
    amount,
    -- Reason: ROW_NUMBER() assigns a unique ascending integer to each row within each user partition.
    -- PARTITION BY user_id resets the counter for each user.
    ROW_NUMBER() OVER (
        PARTITION BY user_id 
        ORDER BY txn_time ASC
    ) AS transaction_seq
FROM user_transactions
ORDER BY user_id ASC, transaction_seq ASC;
```

## Python Implementation
```python
import pandas as pd

user_transactions = pd.DataFrame({
    'txn_id': ['TXN-101', 'TXN-102', 'TXN-103', 'TXN-104', 'TXN-105', 'TXN-106'],
    'user_id': [1, 1, 1, 2, 2, 3],
    'txn_time': ['2024-01-01 08:30:00', '2024-01-02 09:15:00', '2024-01-05 14:20:00', '2024-01-01 11:00:00', '2024-01-03 16:45:00', '2024-01-02 10:10:00'],
    'amount': [45.00, 120.00, 60.00, 300.00, 85.00, 500.00]
})

user_transactions['txn_time'] = pd.to_datetime(user_transactions['txn_time'])

# Reason: Sort chronologically before assigning cumulative counts
df_sorted = user_transactions.sort_values(by=['user_id', 'txn_time']).reset_index(drop=True)

# Reason: .groupby('user_id').cumcount() generates 0-indexed ranking; adding 1 aligns with SQL 1-indexed ROW_NUMBER
df_sorted['transaction_seq'] = df_sorted.groupby('user_id').cumcount() + 1

print(df_sorted)
```
