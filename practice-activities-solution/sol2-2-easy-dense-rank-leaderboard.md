# Solution 2-2 (Easy): Regional Sales Leaderboard with DENSE_RANK

## SQL Implementation
```sql
SELECT 
    rep_id,
    rep_name,
    region,
    closed_revenue,
    -- Reason: DENSE_RANK() assigns consecutive ranks for ties without gaps (e.g. 1, 1, 2)
    DENSE_RANK() OVER (
        PARTITION BY region 
        ORDER BY closed_revenue DESC
    ) AS regional_rank
FROM sales_reps
ORDER BY region ASC, regional_rank ASC;
```

## Python Implementation
```python
import pandas as pd

sales_reps = pd.DataFrame({
    'rep_id': [1, 2, 3, 4, 5, 6, 7],
    'rep_name': ['Alice Walker', 'Bob Stone', 'Charlie Hayes', 'Diana Prince', 'Evan Wright', 'Fiona Gallagher', 'George Clark'],
    'region': ['North', 'North', 'North', 'North', 'South', 'South', 'South'],
    'closed_revenue': [150000.00, 120000.00, 150000.00, 95000.00, 180000.00, 180000.00, 130000.00]
})

# Reason: Replicate SQL DENSE_RANK partitioned by region
# method='dense' ensures consecutive rank integers upon ties; ascending=False ranks highest revenue first
sales_reps['regional_rank'] = (
    sales_reps.groupby('region')['closed_revenue']
    .rank(method='dense', ascending=False)
    .astype(int)
)

# Reason: Sort results to match presentation requirements
result_df = sales_reps.sort_values(by=['region', 'regional_rank']).reset_index(drop=True)
print(result_df)
```
