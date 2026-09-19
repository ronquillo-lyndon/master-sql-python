# Activity 1-3 (Easy): Departmental Salary Benchmarks

## Problem Scenario
Human Resources wants to audit the internal compensation structure across organizational departments recorded in the `employees` table. To establish baseline compensation bands, leadership needs a summary per department displaying the total headcount, the minimum salary, the maximum salary, and the average salary rounded to two decimal places.

### Data Schema Overview
- **`employees` Table**: `emp_id` (INT), `emp_name` (VARCHAR), `dept_name` (VARCHAR), `salary` (DECIMAL)

### Objectives
1. Group employees by `dept_name`.
2. Compute `headcount` (COUNT), `min_salary` (MIN), `max_salary` (MAX), and `avg_salary` (AVG rounded to 2 decimals).
3. Order the report alphabetically by department name.

## Hints
- Aggregation functions collapse multiple employee rows into a single departmental metric row.
- Non-aggregated columns selected in the query must be specified in the grouping expression.
- In Pandas, consider using `.agg()` with dictionary or named tuples alongside NumPy vectorized functions (`np.mean`, `np.min`, `np.max`).
