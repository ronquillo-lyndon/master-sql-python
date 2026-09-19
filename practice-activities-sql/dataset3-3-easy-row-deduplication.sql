-- Dataset 3-3: Duplicate Webhook Events
DROP TABLE IF EXISTS payment_webhooks;

CREATE TABLE payment_webhooks (
    record_id INT PRIMARY KEY,
    event_id VARCHAR(30),
    txn_ref VARCHAR(30),
    amount DECIMAL(10, 2),
    received_at TIMESTAMP
);

INSERT INTO payment_webhooks (record_id, event_id, txn_ref, amount, received_at) VALUES
(1, 'EVT-101', 'TXN-9001', 120.50, '2024-03-01 12:00:01'),
(2, 'EVT-101', 'TXN-9001', 120.50, '2024-03-01 12:00:03'),
(3, 'EVT-102', 'TXN-9002', 85.00, '2024-03-01 12:05:10'),
(4, 'EVT-103', 'TXN-9003', 340.00, '2024-03-01 12:10:00'),
(5, 'EVT-103', 'TXN-9003', 340.00, '2024-03-01 12:10:02');
