-- Dataset 2-1: User Transaction Chronology (ROW_NUMBER)
DROP TABLE IF EXISTS user_transactions;

CREATE TABLE user_transactions (
    txn_id VARCHAR(20) PRIMARY KEY,
    user_id INT,
    txn_time TIMESTAMP,
    amount DECIMAL(10, 2)
);

INSERT INTO user_transactions (txn_id, user_id, txn_time, amount) VALUES
('TXN-101', 1, '2024-01-01 08:30:00', 45.00),
('TXN-102', 1, '2024-01-02 09:15:00', 120.00),
('TXN-103', 1, '2024-01-05 14:20:00', 60.00),
('TXN-104', 2, '2024-01-01 11:00:00', 300.00),
('TXN-105', 2, '2024-01-03 16:45:00', 85.00),
('TXN-106', 3, '2024-01-02 10:10:00', 500.00);
