-- Dataset 2-2: Monthly Sales Performance (DENSE_RANK)
DROP TABLE IF EXISTS sales_reps;

CREATE TABLE sales_reps (
    rep_id INT PRIMARY KEY,
    rep_name VARCHAR(50),
    region VARCHAR(30),
    closed_revenue DECIMAL(10, 2)
);

INSERT INTO sales_reps (rep_id, rep_name, region, closed_revenue) VALUES
(1, 'Alice Walker', 'North', 150000.00),
(2, 'Bob Stone', 'North', 120000.00),
(3, 'Charlie Hayes', 'North', 150000.00),
(4, 'Diana Prince', 'North', 95000.00),
(5, 'Evan Wright', 'South', 180000.00),
(6, 'Fiona Gallagher', 'South', 180000.00),
(7, 'George Clark', 'South', 130000.00);
