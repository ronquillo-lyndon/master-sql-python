-- Dataset 2-9: Equities Closing Price Stream (Weighted Moving Average)
DROP TABLE IF EXISTS stock_price_history;

CREATE TABLE stock_price_history (
    trade_date DATE PRIMARY KEY,
    ticker VARCHAR(10),
    close_price DECIMAL(10, 2)
);

INSERT INTO stock_price_history (trade_date, ticker, close_price) VALUES
('2024-03-01', 'ACME', 100.00),
('2024-03-04', 'ACME', 105.00),
('2024-03-05', 'ACME', 102.50),
('2024-03-06', 'ACME', 110.00),
('2024-03-07', 'ACME', 108.00),
('2024-03-08', 'ACME', 115.00),
('2024-03-11', 'ACME', 118.50),
('2024-03-12', 'ACME', 114.00);
