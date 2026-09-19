# Activity 2-7 (Medium): Departmental Salary Differential Analysis

## Problem Scenario
The compensation committee tracks staff pay in `employee_compensation`. Management wants to evaluate internal equity by comparing each employee's individual base salary directly against their departmental average. For each employee, display their department name, individual salary, the department's average salary, and the salary difference (`base_salary - dept_avg_salary`). The query must not collapse individual employee rows.

### Data Schema Overview
- **`employee_compensation` Table**: `emp_id` (INT), `name` (VARCHAR), `dept_name` (VARCHAR), `base_salary` (DECIMAL)

### Objectives
1. Compute the department average salary using an unconstrained window partition (`OVER (PARTITION BY dept_name)`).
2. Calculate the salary difference between the employee's salary and their department average.
3. Round monetary figures to two decimal places.
4. Order the output by `dept_name` ascending, then `base_salary` descending.

## Hints
- Omitting `ORDER BY` and frame clauses in an `OVER (PARTITION BY ...)` specification calculates the aggregate across the entire partition without sliding.
- In Pandas, this operation is accomplished using `.groupby('dept_name')['base_salary'].transform('mean')`, which broadcasts the group mean back to the original DataFrame rows.
