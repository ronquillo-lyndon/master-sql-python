# Solution 3-6 (Medium): Skew-Resistant Median Imputation

## Python Implementation (Pandas Imputation Pipeline)
```python
import pandas as pd
import numpy as np

delivery_performance = pd.DataFrame({
    'delivery_id': ['DEL-01', 'DEL-02', 'DEL-03', 'DEL-04', 'DEL-05', 'DEL-06', 'DEL-07', 'DEL-08'],
    'carrier': ['SpeedyFreight'] * 8,
    'transit_days': [2.0, 3.0, 2.5, np.nan, 19.0, 3.0, np.nan, 2.8]
})

# Reason: 1. Quality control check - identify missingness volume
missing_count = delivery_performance['transit_days'].isna().sum()
print(f"[QC] Detected {missing_count} missing delivery records.")

# Reason: 2. Calculate median (robust against the 19.0 outlier skew)
computed_median = delivery_performance['transit_days'].median()
print(f"[Imputation] Computed Median: {computed_median:.2f} days (vs Mean: {delivery_performance['transit_days'].mean():.2f} days)")

# Reason: 3. Create boolean flag identifying imputed records before filling
delivery_performance['is_imputed'] = delivery_performance['transit_days'].isna()

# Reason: 4. Impute missing slots with computed median
delivery_performance['cleaned_transit_days'] = delivery_performance['transit_days'].fillna(computed_median)

print(delivery_performance[['delivery_id', 'carrier', 'cleaned_transit_days', 'is_imputed']])
```

## SQL Implementation (DuckDB / Analytical SQL)
```sql
WITH median_calc AS (
    -- Reason: Calculate median transit time across valid observations
    SELECT MEDIAN(transit_days) AS median_transit
    FROM delivery_performance
    WHERE transit_days IS NOT NULL
)
SELECT 
    d.delivery_id,
    d.carrier,
    -- Reason: COALESCE replaces NULLs with the scalar median value from the CTE
    COALESCE(d.transit_days, m.median_transit) AS cleaned_transit_days,
    -- Reason: Boolean flag recording whether value was imputed
    CASE WHEN d.transit_days IS NULL THEN TRUE ELSE FALSE END AS is_imputed
FROM delivery_performance d
CROSS JOIN median_calc m
ORDER BY d.delivery_id ASC;
```
