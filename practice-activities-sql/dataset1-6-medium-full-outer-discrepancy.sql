-- Dataset 1-6: Discrepancy Audit between Legacy ERP and Cloud WMS
DROP TABLE IF EXISTS legacy_shipments;
DROP TABLE IF EXISTS platform_receipts;

CREATE TABLE legacy_shipments (
    tracking_number VARCHAR(30) PRIMARY KEY,
    erp_cost DECIMAL(10, 2),
    shipper_name VARCHAR(40)
);

CREATE TABLE platform_receipts (
    tracking_number VARCHAR(30) PRIMARY KEY,
    billed_amount DECIMAL(10, 2),
    carrier_status VARCHAR(30)
);

INSERT INTO legacy_shipments (tracking_number, erp_cost, shipper_name) VALUES
('TRK-1001', 45.50, 'FedEx'),
('TRK-1002', 120.00, 'UPS'),
('TRK-1003', 85.20, 'DHL'),
('TRK-1004', 33.10, 'USPS'),
('TRK-1005', 210.00, 'FreightOne');

INSERT INTO platform_receipts (tracking_number, billed_amount, carrier_status) VALUES
('TRK-1001', 45.50, 'Delivered'),
('TRK-1002', 125.00, 'Delivered'),
('TRK-1003', 85.20, 'In Transit'),
('TRK-1006', 74.00, 'Delivered'),
('TRK-1007', 150.00, 'Exception');
