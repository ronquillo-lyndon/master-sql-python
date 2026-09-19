-- Dataset 2-10: Customer Lifecycle & Purchase Intervals
DROP TABLE IF EXISTS customer_purchases;
DROP TABLE IF EXISTS customer_signups;

CREATE TABLE customer_signups (
    customer_id INT PRIMARY KEY,
    signup_date DATE,
    channel VARCHAR(30)
);

CREATE TABLE customer_purchases (
    purchase_id INT PRIMARY KEY,
    customer_id INT,
    purchase_date DATE,
    amount DECIMAL(10, 2)
);

INSERT INTO customer_signups (customer_id, signup_date, channel) VALUES
(1, '2024-01-01', 'Organic'),
(2, '2024-01-02', 'Paid Search'),
(3, '2024-01-05', 'Referral'),
(4, '2024-01-10', 'Organic');

INSERT INTO customer_purchases (purchase_id, customer_id, purchase_date, amount) VALUES
(101, 1, '2024-01-03', 50.00),
(102, 1, '2024-01-20', 80.00),
(103, 1, '2024-02-15', 120.00),
(104, 2, '2024-01-04', 300.00),
(105, 2, '2024-01-05', 150.00),
(106, 3, '2024-01-12', 45.00);
