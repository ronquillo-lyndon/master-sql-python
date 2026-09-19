# Solution 2-7 (Medium): Departmental Salary Differential Analysis

## SQL Implementation
```sql
SELECT 
    emp_id,
    name,
    dept_name,
    base_salary,
    -- Reason: Compute full departmental average across all members of the partition without row collapse
    ROUND(AVG(base_salary) OVER (
        PARTITION BY dept_name
    ), 2) AS dept_avg_salary,
    -- Reason: Calculate the differential against the departmental baseline
    ROUND(base_salary - AVG(base_salary) OVER (
        PARTITION BY dept_name
    ), 2) AS salary_diff_from_avg
FROM employee_compensation
ORDER BY dept_name ASC, base_salary DESC;
```

## Python Implementation
```python
import pandas as pd

employee_compensation = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'name': ['Alice Cooper', 'Bob Martin', 'Charlie Daniels', 'Diana Ross', 'Edward Norton', 'Fiona Apple', 'Gordon Ramsay', 'Hannah Abbott'],
    'dept_name': ['Engineering', 'Engineering', 'Engineering', 'Finance', 'Finance', 'Marketing', 'Marketing', 'Marketing'],
    'base_salary': [130000.00, 110000.00, 150000.00, 95000.00, 105000.00, 88000.00, 92000.00, 115000.00]
})

# Reason: Replicate SQL PARTITION BY aggregate broadcast using .transform('mean')
# .transform preserves original row dimensions
employee_compensation['dept_avg_salary'] = (
    employee_compensation.groupby('dept_name')['base_salary']
    .transform('mean')
    .round(2)
)

# Reason: Vectorized calculation of salary disparity
employee_compensation['salary_diff_from_avg'] = (
    employee_compensation['base_salary'] - employee_compensation['dept_avg_salary']
).round(2)

result_df = employee_compensation.sort_values(by=['dept_name', 'base_salary'], ascending=[True, False])
print(result_df)
```
