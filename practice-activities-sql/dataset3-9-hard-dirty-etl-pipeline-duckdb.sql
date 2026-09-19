-- Dataset 3-9: Raw Messy Point-of-Sale Transactions & Store Dimension
DROP TABLE IF EXISTS raw_pos_transactions;
DROP TABLE IF EXISTS store_dimension;

CREATE TABLE store_dimension (
    store_code VARCHAR(20) PRIMARY KEY,
    city VARCHAR(50),
    tax_rate DECIMAL(4, 3)
);

CREATE TABLE raw_pos_transactions (
    receipt_id VARCHAR(30),
    raw_store VARCHAR(30),
    raw_cashier VARCHAR(50),
    sale_amount DECIMAL(10, 2),
    txn_date VARCHAR(30)
);

INSERT INTO store_dimension (store_code, city, tax_rate) VALUES
('STORE-NY', 'New York', 0.088),
('STORE-CA', 'San Francisco', 0.095),
('STORE-TX', 'Austin', 0.082);

INSERT INTO raw_pos_transactions (receipt_id, raw_store, raw_cashier, sale_amount, txn_date) VALUES
('RCP-001', ' STORE-NY ', '  JOHN DOE  ', 150.00, '2024-02-01'),
('RCP-001', ' STORE-NY ', '  JOHN DOE  ', 150.00, '2024-02-01'),
('RCP-002', 'store-ca', 'alice smith', NULL, '2024-02-01'),
('RCP-003', 'STORE-TX', 'bob johnson', 320.50, '2024-02-02'),
('RCP-004', ' STORE-NY', 'John Doe ', 95.00, '2024-02-02'),
('RCP-005', 'STORE-UNKNOWN', 'charlie', 210.00, '2024-02-03');
