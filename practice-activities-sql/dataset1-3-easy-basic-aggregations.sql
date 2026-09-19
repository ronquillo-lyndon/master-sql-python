-- Dataset 1-3: Departmental Salary Benchmarks
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    dept_name VARCHAR(40),
    salary DECIMAL(10, 2)
);

INSERT INTO employees (emp_id, emp_name, dept_name, salary) VALUES
(1, 'Sarah Chen', 'Engineering', 125000.00),
(2, 'Dave Miller', 'Engineering', 140000.00),
(3, 'Elena Rostova', 'Engineering', 110000.00),
(4, 'Marcus Brody', 'Marketing', 85000.00),
(5, 'Chloe Price', 'Marketing', 92000.00),
(6, 'Tom Alvarez', 'Sales', 78000.00),
(7, 'Priya Patel', 'Sales', 105000.00),
(8, 'Liam Vance', 'Sales', 96000.00);
