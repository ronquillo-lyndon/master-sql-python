# Solution 3-3 (Easy): Payment Webhook Deduplication Pipeline

## SQL Implementation
```sql
WITH ranked_webhooks AS (
    SELECT 
        record_id,
        event_id,
        txn_ref,
        amount,
        received_at,
        -- Reason: Enumerate occurrences per event_id chronologically
        ROW_NUMBER() OVER (
            PARTITION BY event_id 
            ORDER BY received_at ASC
        ) AS delivery_attempt
    FROM payment_webhooks
)
-- Reason: Retain only the initial webhook notification (attempt #1)
SELECT 
    record_id,
    event_id,
    txn_ref,
    amount,
    received_at
FROM ranked_webhooks
WHERE delivery_attempt = 1
ORDER BY record_id ASC;
```

## Python Implementation
```python
import pandas as pd

payment_webhooks = pd.DataFrame({
    'record_id': [1, 2, 3, 4, 5],
    'event_id': ['EVT-101', 'EVT-101', 'EVT-102', 'EVT-103', 'EVT-103'],
    'txn_ref': ['TXN-9001', 'TXN-9001', 'TXN-9002', 'TXN-9003', 'TXN-9003'],
    'amount': [120.50, 120.50, 85.00, 340.00, 340.00],
    'received_at': ['2024-03-01 12:00:01', '2024-03-01 12:00:03', '2024-03-01 12:05:10', '2024-03-01 12:10:00', '2024-03-01 12:10:02']
})

payment_webhooks['received_at'] = pd.to_datetime(payment_webhooks['received_at'])

# Reason: Ensure dataset is strictly sorted by arrival timestamp before deduplication
payment_webhooks = payment_webhooks.sort_values(by='received_at').reset_index(drop=True)

# Reason: Check duplicate volume for pipeline telemetry
duplicate_count = payment_webhooks.duplicated(subset=['event_id']).sum()
print(f"[QC] Dropping {duplicate_count} duplicate webhook delivery attempt(s).")

# Reason: Replicate SQL WHERE row_num = 1 using drop_duplicates keep='first'
clean_webhooks = payment_webhooks.drop_duplicates(subset=['event_id'], keep='first').sort_values(by='record_id')

print(clean_webhooks)
```
