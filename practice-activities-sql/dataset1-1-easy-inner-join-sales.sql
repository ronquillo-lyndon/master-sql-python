-- Dataset 1-1: Active Customers and Orders (Inner Join)
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(50),
    segment VARCHAR(30)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10, 2)
);

INSERT INTO customers (customer_id, name, segment) VALUES
(1, 'Alice Corp', 'Enterprise'),
(2, 'Bob Labs', 'SMB'),
(3, 'Charlie Retail', 'Retail'),
(4, 'Delta Inc', 'SMB'),
(5, 'Echo Solutions', 'Enterprise');

INSERT INTO orders (order_id, customer_id, order_date, amount) VALUES
(101, 1, '2024-01-10', 1250.00),
(102, 1, '2024-01-15', 850.50),
(103, 2, '2024-01-16', 320.00),
(104, 3, '2024-01-20', 150.00),
(105, 3, '2024-01-22', 90.00),
(106, 99, '2024-01-25', 500.00); -- Unmatched orphan order
