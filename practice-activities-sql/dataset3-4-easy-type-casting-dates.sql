-- Dataset 3-4: Untyped String Invoices
DROP TABLE IF EXISTS raw_staging_invoices;

CREATE TABLE raw_staging_invoices (
    invoice_id VARCHAR(20) PRIMARY KEY,
    string_date VARCHAR(30),
    raw_amount_str VARCHAR(30)
);

INSERT INTO raw_staging_invoices (invoice_id, string_date, raw_amount_str) VALUES
('INV-801', '2024-01-15', '1450.50'),
('INV-802', '2024-01-16', '320.00'),
('INV-803', '2024-01-20', '890.75'),
('INV-804', '2024-01-22', '1100.00'),
('INV-805', '2024-01-25', '45.25');
