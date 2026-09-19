-- Dataset 1-8: Payment Method Breakdown
DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    txn_id VARCHAR(20) PRIMARY KEY,
    customer_id INT,
    payment_method VARCHAR(30),
    amount DECIMAL(10, 2),
    status VARCHAR(20)
);

INSERT INTO transactions (txn_id, customer_id, payment_method, amount, status) VALUES
('TXN-01', 1, 'Credit Card', 150.00, 'Completed'),
('TXN-02', 2, 'PayPal', 80.00, 'Completed'),
('TXN-03', 1, 'Credit Card', 200.00, 'Completed'),
('TXN-04', 3, 'Bank Wire', 1200.00, 'Completed'),
('TXN-05', 4, 'Credit Card', 50.00, 'Refunded'),
('TXN-06', 2, 'PayPal', 120.00, 'Completed'),
('TXN-07', 5, 'Apple Pay', 95.00, 'Completed'),
('TXN-08', 3, 'Bank Wire', 3400.00, 'Completed'),
('TXN-09', 1, 'Apple Pay', 40.00, 'Completed');
