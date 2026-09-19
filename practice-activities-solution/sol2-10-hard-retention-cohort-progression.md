# Solution 2-10 (Hard): Customer Retention & Purchase Interval Pipeline

## SQL Implementation
```sql
WITH customer_order_stream AS (
    SELECT 
        s.customer_id,
        s.signup_date,
        s.channel,
        p.purchase_id,
        p.purchase_date,
        p.amount,
        -- Reason: Assign order sequence for each customer; NULL for non-purchasing customers
        CASE 
            WHEN p.purchase_id IS NOT NULL THEN 
                ROW_NUMBER() OVER (PARTITION BY s.customer_id ORDER BY p.purchase_date ASC)
            ELSE 0 
        END AS order_seq,
        -- Reason: Retrieve previous purchase date for the customer
        LAG(p.purchase_date, 1) OVER (PARTITION BY s.customer_id ORDER BY p.purchase_date ASC) AS prior_purchase_date
    FROM customer_signups s
    -- Reason: LEFT JOIN preserves non-purchasing customers like customer 4
    LEFT JOIN customer_purchases p 
        ON s.customer_id = p.customer_id
)
SELECT 
    customer_id,
    channel,
    signup_date,
    purchase_id,
    purchase_date,
    COALESCE(amount, 0.00) AS amount,
    order_seq,
    -- Reason: Calculate day interval since prior purchase; 0 for first order or non-purchasers
    CASE 
        WHEN prior_purchase_date IS NOT NULL THEN (CAST(purchase_date AS DATE) - CAST(prior_purchase_date AS DATE))
        ELSE 0 
    END AS days_since_prior_purchase
FROM customer_order_stream
ORDER BY customer_id ASC, order_seq ASC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

customer_signups = pd.DataFrame({
    'customer_id': [1, 2, 3, 4],
    'signup_date': ['2024-01-01', '2024-01-02', '2024-01-05', '2024-01-10'],
    'channel': ['Organic', 'Paid Search', 'Referral', 'Organic']
})

customer_purchases = pd.DataFrame({
    'purchase_id': [101, 102, 103, 104, 105, 106],
    'customer_id': [1, 1, 1, 2, 2, 3],
    'purchase_date': ['2024-01-03', '2024-01-20', '2024-02-15', '2024-01-04', '2024-01-05', '2024-01-12'],
    'amount': [50.00, 80.00, 120.00, 300.00, 150.00, 45.00]
})

# Reason: Step 1 - Relational LEFT JOIN to preserve inactive signups
merged_df = pd.merge(customer_signups, customer_purchases, on='customer_id', how='left')

# Convert dates to datetime
merged_df['purchase_date'] = pd.to_datetime(merged_df['purchase_date'])
merged_df['signup_date'] = pd.to_datetime(merged_df['signup_date'])
merged_df = merged_df.sort_values(by=['customer_id', 'purchase_date']).reset_index(drop=True)

# Reason: Step 2 - Compute order sequence per customer (0 for non-purchasers)
merged_df['order_seq'] = np.where(
    merged_df['purchase_id'].notna(),
    merged_df.groupby('customer_id').cumcount() + 1,
    0
)

# Reason: Step 3 - Shift purchase date to get prior purchase date
merged_df['prior_purchase_date'] = merged_df.groupby('customer_id')['purchase_date'].shift(1)

# Reason: Step 4 - Calculate days difference; fill NaN with 0
day_diff = (merged_df['purchase_date'] - merged_df['prior_purchase_date']).dt.days
merged_df['days_since_prior_purchase'] = day_diff.fillna(0).astype(int)

# Reason: Resolve unpurchased amounts
merged_df['amount'] = merged_df['amount'].fillna(0.00)

print(merged_df[['customer_id', 'channel', 'purchase_id', 'purchase_date', 'amount', 'order_seq', 'days_since_prior_purchase']])
```
