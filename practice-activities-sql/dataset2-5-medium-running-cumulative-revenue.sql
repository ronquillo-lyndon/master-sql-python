-- Dataset 2-5: Daily SaaS Bookings (Cumulative Sum)
DROP TABLE IF EXISTS daily_financials;

CREATE TABLE daily_financials (
    record_date DATE PRIMARY KEY,
    new_subscribers INT,
    daily_revenue DECIMAL(10, 2)
);

INSERT INTO daily_financials (record_date, new_subscribers, daily_revenue) VALUES
('2024-01-01', 12, 1200.00),
('2024-01-02', 18, 1850.00),
('2024-01-03', 15, 1400.00),
('2024-01-04', 22, 2300.00),
('2024-01-05', 30, 3100.00),
('2024-01-06', 25, 2750.00),
('2024-01-07', 28, 2900.00),
('2024-01-08', 35, 3800.00);
