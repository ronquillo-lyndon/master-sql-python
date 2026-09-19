-- Dataset 3-8: Financial Ledger Staging Records
DROP TABLE IF EXISTS daily_ledger_staging;

CREATE TABLE daily_ledger_staging (
    entry_id INT PRIMARY KEY,
    account_code VARCHAR(20),
    entry_date DATE,
    amount DECIMAL(10, 2)
);

INSERT INTO daily_ledger_staging (entry_id, account_code, entry_date, amount) VALUES
(1001, 'ACC-ASSET-01', '2024-03-01', 1500.00),
(1002, 'ACC-LIAB-02', '2024-03-01', -500.00),
(1003, 'ACC-REV-03', '2024-03-01', 2800.00),
(1004, 'ACC-EXP-04', '2024-03-01', -750.00);
