-- Dataset 2-8: Order Funnel Multi-Step Pipeline (CTE)
DROP TABLE IF EXISTS store_orders;

CREATE TABLE store_orders (
    order_id INT PRIMARY KEY,
    store_id INT,
    order_timestamp TIMESTAMP,
    order_value DECIMAL(10, 2)
);

INSERT INTO store_orders (order_id, store_id, order_timestamp, order_value) VALUES
(1, 101, '2024-02-01 10:15:00', 45.00),
(2, 101, '2024-02-01 14:20:00', 120.00),
(3, 101, '2024-02-02 09:30:00', 310.00),
(4, 102, '2024-02-01 11:00:00', 80.00),
(5, 102, '2024-02-02 16:00:00', 520.00),
(6, 102, '2024-02-02 18:30:00', 140.00),
(7, 103, '2024-02-01 08:45:00', 950.00),
(8, 103, '2024-02-02 12:10:00', 400.00);
