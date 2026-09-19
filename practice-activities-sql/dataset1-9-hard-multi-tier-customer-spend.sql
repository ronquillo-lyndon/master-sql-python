-- Dataset 1-9: Customer, Orders, Line Items, and Categories
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(50),
    tier VARCHAR(20)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(30)
);

CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10, 2)
);

INSERT INTO customers (customer_id, name, tier) VALUES
(1, 'Alpha Corp', 'Gold'),
(2, 'Beta Tech', 'Silver'),
(3, 'Gamma LLC', 'Bronze'),
(4, 'Delta Health', 'Gold'),
(5, 'Epsilon Retail', 'Bronze');

INSERT INTO products (product_id, product_name, category) VALUES
(101, 'Cloud Server Blade', 'Infrastructure'),
(102, 'Network Switch 48P', 'Networking'),
(103, 'SaaS Annual Seat', 'Software'),
(104, 'Support Ticket Pack', 'Services');

INSERT INTO orders (order_id, customer_id, order_date) VALUES
(5001, 1, '2024-01-15'),
(5002, 1, '2024-02-10'),
(5003, 2, '2024-01-20'),
(5004, 3, '2024-02-12');

INSERT INTO order_items (item_id, order_id, product_id, quantity, unit_price) VALUES
(1, 5001, 101, 2, 1500.00),
(2, 5001, 102, 1, 800.00),
(3, 5002, 103, 5, 250.00),
(4, 5003, 104, 2, 400.00),
(5, 5004, 101, 1, 1500.00);
