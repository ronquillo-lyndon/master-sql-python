-- Dataset 1-2: Customer Directory with Inactive Accounts (Left Join)
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    company_name VARCHAR(60),
    region VARCHAR(30)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_value DECIMAL(10, 2)
);

INSERT INTO customers (customer_id, company_name, region) VALUES
(1, 'Apex Logistics', 'North'),
(2, 'Beacon Systems', 'West'),
(3, 'Cascade Media', 'East'),
(4, 'Dune Ventures', 'South'),
(5, 'Evergreen Partners', 'North');

INSERT INTO orders (order_id, customer_id, order_value) VALUES
(501, 1, 450.00),
(502, 1, 950.00),
(503, 3, 120.00);
