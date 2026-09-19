-- Dataset 3-7: Supplier Wholesale Catalog
DROP TABLE IF EXISTS supplier_catalog;

CREATE TABLE supplier_catalog (
    sku VARCHAR(30) PRIMARY KEY,
    brand VARCHAR(40),
    wholesale_price DECIMAL(10, 2),
    available_stock INT
);

INSERT INTO supplier_catalog (sku, brand, wholesale_price, available_stock) VALUES
('SUP-101', 'LogiPro', 45.00, 250),
('SUP-102', 'LogiPro', 85.50, 140),
('SUP-103', 'AnkerPower', 25.00, 500),
('SUP-104', 'AnkerPower', 65.00, 180),
('SUP-105', 'KeySonic', 110.00, 95);
