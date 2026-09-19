# Solution 1-3 (Easy): Departmental Salary Benchmarks

## SQL Implementation
```sql
SELECT 
    dept_name,
    -- Reason: Count total employee records per department group
    COUNT(emp_id) AS headcount,
    -- Reason: Compute the lowest compensation boundary in the department
    MIN(salary) AS min_salary,
    -- Reason: Compute the highest compensation boundary in the department
    MAX(salary) AS max_salary,
    -- Reason: Compute arithmetic mean salary and round to 2 decimal places
    ROUND(AVG(salary), 2) AS avg_salary
FROM employees
-- Reason: Collapse row-level employee data into department groups
GROUP BY dept_name
ORDER BY dept_name ASC;
```

## Python Implementation
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'emp_name': ['Sarah Chen', 'Dave Miller', 'Elena Rostova', 'Marcus Brody', 'Chloe Price', 'Tom Alvarez', 'Priya Patel', 'Liam Vance'],
    'dept_name': ['Engineering', 'Engineering', 'Engineering', 'Marketing', 'Marketing', 'Sales', 'Sales', 'Sales'],
    'salary': [125000.00, 140000.00, 110000.00, 85000.00, 92000.00, 78000.00, 105000.00, 96000.00]
})

# Reason: Replicate SQL GROUP BY using .groupby() and vectorized NumPy aggregations
dept_summary = employees.groupby('dept_name').agg(
    headcount=('emp_id', 'count'),
    min_salary=('salary', np.min),
    max_salary=('salary', np.max),
    avg_salary=('salary', np.mean)
).reset_index()

# Reason: Round avg_salary to 2 decimal places and sort alphabetically
dept_summary['avg_salary'] = dept_summary['avg_salary'].round(2)
dept_summary = dept_summary.sort_values(by='dept_name', ascending=True)

print(dept_summary)
```
