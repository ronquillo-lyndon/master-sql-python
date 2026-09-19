# Solution 3-5 (Medium): Customer Retention Segmentation with CASE WHEN

## SQL Implementation
```sql
SELECT 
    customer_id,
    company_name,
    lifetime_spend,
    days_since_last_login,
    -- Reason: Conditional branching evaluates customer value and engagement tiers
    CASE 
        WHEN lifetime_spend >= 20000.00 AND days_since_last_login <= 30 THEN 'VIP Active'
        WHEN lifetime_spend >= 20000.00 AND days_since_last_login > 30 THEN 'VIP Churn Risk'
        WHEN lifetime_spend < 20000.00 AND days_since_last_login <= 30 THEN 'Standard Active'
        ELSE 'Standard Dormant'
    END AS account_health_tier
FROM customer_activity
ORDER BY lifetime_spend DESC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

customer_activity = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5, 6],
    'company_name': ['Alpha Tech', 'Beta Logistics', 'Gamma Global', 'Delta Dynamics', 'Epsilon Retail', 'Zeta Health'],
    'lifetime_spend': [25000.00, 4500.00, 85000.00, 800.00, 12000.00, 500.00],
    'days_since_last_login': [4, 45, 2, 120, 18, 5]
})

# Reason: Define vectorized conditions and matching choices matching SQL CASE WHEN
conditions = [
    (customer_activity['lifetime_spend'] >= 20000.00) & (customer_activity['days_since_last_login'] <= 30),
    (customer_activity['lifetime_spend'] >= 20000.00) & (customer_activity['days_since_last_login'] > 30),
    (customer_activity['lifetime_spend'] < 20000.00) & (customer_activity['days_since_last_login'] <= 30),
    (customer_activity['lifetime_spend'] < 20000.00) & (customer_activity['days_since_last_login'] > 30)
]

choices = ['VIP Active', 'VIP Churn Risk', 'Standard Active', 'Standard Dormant']

customer_activity['account_health_tier'] = np.select(conditions, choices, default='Unclassified')

result_df = customer_activity.sort_values(by='lifetime_spend', ascending=False)
print(result_df)
```
