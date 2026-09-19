# Solution 1-8 (Medium): Payment Channel Breakdown & Settlement

## SQL Implementation
```sql
SELECT 
    payment_method,
    -- Reason: Count total attempted transactions
    COUNT(txn_id) AS total_attempts,
    -- Reason: Count distinct customers who utilized this payment channel
    COUNT(DISTINCT customer_id) AS unique_customers,
    -- Reason: Conditional SUM calculates settled revenue only for completed transactions
    COALESCE(SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END), 0.00) AS completed_volume,
    -- Reason: Conditional SUM/COUNT counts records where status is Refunded
    SUM(CASE WHEN status = 'Refunded' THEN 1 ELSE 0 END) AS refunded_count
FROM transactions
GROUP BY payment_method
ORDER BY completed_volume DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

transactions = pd.DataFrame({
    'txn_id': ['TXN-01', 'TXN-02', 'TXN-03', 'TXN-04', 'TXN-05', 'TXN-06', 'TXN-07', 'TXN-08', 'TXN-09'],
    'customer_id': [1, 2, 1, 3, 4, 2, 5, 3, 1],
    'payment_method': ['Credit Card', 'PayPal', 'Credit Card', 'Bank Wire', 'Credit Card', 'PayPal', 'Apple Pay', 'Bank Wire', 'Apple Pay'],
    'amount': [150.00, 80.00, 200.00, 1200.00, 50.00, 120.00, 95.00, 3400.00, 40.00],
    'status': ['Completed', 'Completed', 'Completed', 'Completed', 'Refunded', 'Completed', 'Completed', 'Completed', 'Completed']
})

# Reason: Create vectorized helper columns for conditional aggregation
transactions['completed_amount'] = np.where(transactions['status'] == 'Completed', transactions['amount'], 0.0)
transactions['is_refunded'] = np.where(transactions['status'] == 'Refunded', 1, 0)

# Reason: Group by payment_method and aggregate metrics
channel_summary = transactions.groupby('payment_method').agg(
    total_attempts=('txn_id', 'count'),
    unique_customers=('customer_id', 'nunique'),
    completed_volume=('completed_amount', np.sum),
    refunded_count=('is_refunded', np.sum)
).reset_index()

channel_summary = channel_summary.sort_values(by='completed_volume', ascending=False)
print(channel_summary)
```
