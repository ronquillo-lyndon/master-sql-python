-- Dataset 3-2: Incomplete Freight Logistics Surcharges
DROP TABLE IF EXISTS shipment_costs;

CREATE TABLE shipment_costs (
    shipment_id VARCHAR(20) PRIMARY KEY,
    base_cost DECIMAL(10, 2),
    fuel_surcharge DECIMAL(10, 2),
    expedite_fee DECIMAL(10, 2)
);

INSERT INTO shipment_costs (shipment_id, base_cost, fuel_surcharge, expedite_fee) VALUES
('SHP-001', 250.00, 35.00, 50.00),
('SHP-002', 400.00, NULL, 0.00),
('SHP-003', 180.00, 20.00, NULL),
('SHP-004', 520.00, NULL, NULL),
('SHP-005', 310.00, 45.00, 25.00);
