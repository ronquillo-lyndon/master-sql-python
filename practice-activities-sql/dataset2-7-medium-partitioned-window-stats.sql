-- Dataset 2-7: Departmental Compensation Distribution
DROP TABLE IF EXISTS employee_compensation;

CREATE TABLE employee_compensation (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    dept_name VARCHAR(40),
    base_salary DECIMAL(10, 2)
);

INSERT INTO employee_compensation (emp_id, name, dept_name, base_salary) VALUES
(1, 'Alice Cooper', 'Engineering', 130000.00),
(2, 'Bob Martin', 'Engineering', 110000.00),
(3, 'Charlie Daniels', 'Engineering', 150000.00),
(4, 'Diana Ross', 'Finance', 95000.00),
(5, 'Edward Norton', 'Finance', 105000.00),
(6, 'Fiona Apple', 'Marketing', 88000.00),
(7, 'Gordon Ramsay', 'Marketing', 92000.00),
(8, 'Hannah Abbott', 'Marketing', 115000.00);
