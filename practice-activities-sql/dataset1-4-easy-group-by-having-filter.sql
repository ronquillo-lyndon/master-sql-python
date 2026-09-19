-- Dataset 1-4: Regional Store Performance
DROP TABLE IF EXISTS store_sales;

CREATE TABLE store_sales (
    sale_id INT PRIMARY KEY,
    store_id INT,
    region VARCHAR(30),
    sale_amount DECIMAL(10, 2),
    sale_date DATE
);

INSERT INTO store_sales (sale_id, store_id, region, sale_amount, sale_date) VALUES
(1, 101, 'North', 1500.00, '2024-02-01'),
(2, 101, 'North', 2300.00, '2024-02-02'),
(3, 102, 'North', 1100.00, '2024-02-01'),
(4, 201, 'South', 600.00, '2024-02-01'),
(5, 201, 'South', 450.00, '2024-02-03'),
(6, 301, 'East', 3200.00, '2024-02-01'),
(7, 301, 'East', 2800.00, '2024-02-04'),
(8, 401, 'West', 750.00, '2024-02-02'),
(9, 402, 'West', 800.00, '2024-02-03');
