-- Dataset 1-10: Multi-channel Inventory Audit
DROP TABLE IF EXISTS purchase_receipts;
DROP TABLE IF EXISTS sales_shipments;
DROP TABLE IF EXISTS current_catalog;

CREATE TABLE current_catalog (
    sku VARCHAR(30) PRIMARY KEY,
    sku_name VARCHAR(60),
    base_cost DECIMAL(10, 2)
);

CREATE TABLE purchase_receipts (
    receipt_id INT PRIMARY KEY,
    sku VARCHAR(30),
    quantity_received INT
);

CREATE TABLE sales_shipments (
    shipment_id INT PRIMARY KEY,
    sku VARCHAR(30),
    quantity_shipped INT
);

INSERT INTO current_catalog (sku, sku_name, base_cost) VALUES
('SKU-A', 'Industrial Router', 180.00),
('SKU-B', 'Optical Transceiver', 45.00),
('SKU-C', 'Patch Panel Cat6', 60.00),
('SKU-D', 'Server Rack 42U', 650.00),
('SKU-E', 'Power Distribution Unit', 120.00);

INSERT INTO purchase_receipts (receipt_id, sku, quantity_received) VALUES
(1, 'SKU-A', 50),
(2, 'SKU-A', 30),
(3, 'SKU-B', 200),
(4, 'SKU-C', 80),
(5, 'SKU-D', 10);

INSERT INTO sales_shipments (shipment_id, sku, quantity_shipped) VALUES
(101, 'SKU-A', 40),
(102, 'SKU-B', 150),
(103, 'SKU-C', 75),
(104, 'SKU-D', 8);


SELECT 
    cc.sku,
    cc.sku_name,
    cc.base_cost,
    COALESCE(SUM(pr.quantity_received), 0.0) as total_received,
    COALESCE(SUM(ss.quantity_shipped), 0.0) as total_shipped,
    COALESCE(COALESCE(SUM(pr.quantity_received), 0.0) 
    - COALESCE(SUM(ss.quantity_shipped), 0.0), 0.0) as net_balance,
    COALESCE(COALESCE(SUM(pr.quantity_received), 0.0) 
    - COALESCE(SUM(ss.quantity_shipped), 0.0), 0.0) 
    * cc.base_cost as inventory_valuation
FROM 
    current_catalog cc
LEFT JOIN 
    purchase_receipts pr 
ON cc.sku = pr.sku
LEFT JOIN 
    sales_shipments ss
ON cc.sku = ss.sku
GROUP BY
    cc.sku, cc.sku_name, cc.base_cost
ORDER BY inventory_valuation desc;