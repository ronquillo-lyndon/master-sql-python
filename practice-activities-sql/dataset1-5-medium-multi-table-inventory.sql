-- Dataset 1-5: Products, Categories, and Warehouse Inventory
DROP TABLE IF EXISTS warehouse_stocks;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(40)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    category_id INT,
    product_name VARCHAR(60),
    unit_price DECIMAL(10, 2)
);

CREATE TABLE warehouse_stocks (
    stock_id INT PRIMARY KEY,
    product_id INT,
    warehouse_code VARCHAR(20),
    quantity_on_hand INT
);

INSERT INTO categories (category_id, category_name) VALUES
(1, 'Electronics'),
(2, 'Apparel'),
(3, 'Office Supplies');

INSERT INTO products (product_id, category_id, product_name, unit_price) VALUES
(10, 1, 'Noise-Cancelling Headphones', 199.99),
(11, 1, 'Ergonomic Mechanical Keyboard', 129.50),
(12, 2, 'Merino Wool Jacket', 180.00),
(13, 2, 'Trail Running Shoes', 110.00),
(14, 3, 'Heavy-Duty Paper Shredder', 85.00),
(15, 3, 'Standing Desk Converter', 210.00);

INSERT INTO warehouse_stocks (stock_id, product_id, warehouse_code, quantity_on_hand) VALUES
(1, 10, 'WH-EAST', 45),
(2, 10, 'WH-WEST', 30),
(3, 11, 'WH-EAST', 60),
(4, 12, 'WH-CENTRAL', 15),
(5, 14, 'WH-WEST', 80),
(6, 15, 'WH-EAST', 25);
