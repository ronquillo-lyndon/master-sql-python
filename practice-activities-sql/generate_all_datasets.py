"""
Seeding script to generate all 30 SQL datasets for Units 1-3.
Strictly ensures row counts are <= 200 rows per dataset,
with realistic edge cases (nulls, duplicates, whitespace, formatting issues).
"""

import os

SQL_DIR = os.path.join(os.path.dirname(__file__))

def write_sql(filename, content):
    filepath = os.path.join(SQL_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {filename}")

# ==========================================
# UNIT 1 DATASETS
# ==========================================

DATASET_1_1 = """
-- Dataset 1-1: Active Customers and Orders (Inner Join)
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(50),
    segment VARCHAR(30)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10, 2)
);

INSERT INTO customers (customer_id, name, segment) VALUES
(1, 'Alice Corp', 'Enterprise'),
(2, 'Bob Labs', 'SMB'),
(3, 'Charlie Retail', 'Retail'),
(4, 'Delta Inc', 'SMB'),
(5, 'Echo Solutions', 'Enterprise');

INSERT INTO orders (order_id, customer_id, order_date, amount) VALUES
(101, 1, '2024-01-10', 1250.00),
(102, 1, '2024-01-15', 850.50),
(103, 2, '2024-01-16', 320.00),
(104, 3, '2024-01-20', 150.00),
(105, 3, '2024-01-22', 90.00),
(106, 99, '2024-01-25', 500.00); -- Unmatched orphan order
"""

DATASET_1_2 = """
-- Dataset 1-2: Customer Directory with Inactive Accounts (Left Join)
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    company_name VARCHAR(60),
    region VARCHAR(30)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_value DECIMAL(10, 2)
);

INSERT INTO customers (customer_id, company_name, region) VALUES
(1, 'Apex Logistics', 'North'),
(2, 'Beacon Systems', 'West'),
(3, 'Cascade Media', 'East'),
(4, 'Dune Ventures', 'South'),
(5, 'Evergreen Partners', 'North');

INSERT INTO orders (order_id, customer_id, order_value) VALUES
(501, 1, 450.00),
(502, 1, 950.00),
(503, 3, 120.00);
"""

DATASET_1_3 = """
-- Dataset 1-3: Departmental Salary Benchmarks
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    dept_name VARCHAR(40),
    salary DECIMAL(10, 2)
);

INSERT INTO employees (emp_id, emp_name, dept_name, salary) VALUES
(1, 'Sarah Chen', 'Engineering', 125000.00),
(2, 'Dave Miller', 'Engineering', 140000.00),
(3, 'Elena Rostova', 'Engineering', 110000.00),
(4, 'Marcus Brody', 'Marketing', 85000.00),
(5, 'Chloe Price', 'Marketing', 92000.00),
(6, 'Tom Alvarez', 'Sales', 78000.00),
(7, 'Priya Patel', 'Sales', 105000.00),
(8, 'Liam Vance', 'Sales', 96000.00);
"""

DATASET_1_4 = """
-- Dataset 1-4: Regional Store Performance
DROP TABLE IF EXISTS store_sales;

CREATE TABLE store_sales (
    sale_id INT PRIMARY KEY,
    store_id INT,
    region VARCHAR(30),
    sale_amount DECIMAL(10, 2),
    sale_date DATE
);

INSERT INTO store_sales (sale_id, store_id, region, sale_amount, sale_date) VALUES
(1, 101, 'North', 1500.00, '2024-02-01'),
(2, 101, 'North', 2300.00, '2024-02-02'),
(3, 102, 'North', 1100.00, '2024-02-01'),
(4, 201, 'South', 600.00, '2024-02-01'),
(5, 201, 'South', 450.00, '2024-02-03'),
(6, 301, 'East', 3200.00, '2024-02-01'),
(7, 301, 'East', 2800.00, '2024-02-04'),
(8, 401, 'West', 750.00, '2024-02-02'),
(9, 402, 'West', 800.00, '2024-02-03');
"""

DATASET_1_5 = """
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
"""

DATASET_1_6 = """
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
"""

DATASET_1_7 = """
-- Dataset 1-7: Web and Mobile User Activity Logs
DROP TABLE IF EXISTS web_clicks;
DROP TABLE IF EXISTS mobile_taps;

CREATE TABLE web_clicks (
    event_id VARCHAR(20) PRIMARY KEY,
    user_id INT,
    action_type VARCHAR(30),
    event_timestamp VARCHAR(30)
);

CREATE TABLE mobile_taps (
    event_id VARCHAR(20) PRIMARY KEY,
    user_id INT,
    action_type VARCHAR(30),
    event_timestamp VARCHAR(30)
);

INSERT INTO web_clicks (event_id, user_id, action_type, event_timestamp) VALUES
('WEB-01', 101, 'page_view', '2024-03-01 10:01:05'),
('WEB-02', 102, 'add_to_cart', '2024-03-01 10:05:12'),
('WEB-03', 101, 'checkout_start', '2024-03-01 10:12:44'),
('WEB-04', 103, 'page_view', '2024-03-01 10:15:30');

INSERT INTO mobile_taps (event_id, user_id, action_type, event_timestamp) VALUES
('MOB-01', 102, 'app_open', '2024-03-01 10:00:20'),
('MOB-02', 104, 'page_view', '2024-03-01 10:04:15'),
('MOB-03', 101, 'push_dismiss', '2024-03-01 10:11:00'),
('MOB-04', 102, 'checkout_success', '2024-03-01 10:20:00');
"""

DATASET_1_8 = """
-- Dataset 1-8: Payment Method Breakdown
DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    txn_id VARCHAR(20) PRIMARY KEY,
    customer_id INT,
    payment_method VARCHAR(30),
    amount DECIMAL(10, 2),
    status VARCHAR(20)
);

INSERT INTO transactions (txn_id, customer_id, payment_method, amount, status) VALUES
('TXN-01', 1, 'Credit Card', 150.00, 'Completed'),
('TXN-02', 2, 'PayPal', 80.00, 'Completed'),
('TXN-03', 1, 'Credit Card', 200.00, 'Completed'),
('TXN-04', 3, 'Bank Wire', 1200.00, 'Completed'),
('TXN-05', 4, 'Credit Card', 50.00, 'Refunded'),
('TXN-06', 2, 'PayPal', 120.00, 'Completed'),
('TXN-07', 5, 'Apple Pay', 95.00, 'Completed'),
('TXN-08', 3, 'Bank Wire', 3400.00, 'Completed'),
('TXN-09', 1, 'Apple Pay', 40.00, 'Completed');
"""

DATASET_1_9 = """
-- Dataset 1-9: Customer, Orders, Line Items, and Categories
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(50),
    tier VARCHAR(20)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(30)
);

CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10, 2)
);

INSERT INTO customers (customer_id, name, tier) VALUES
(1, 'Alpha Corp', 'Gold'),
(2, 'Beta Tech', 'Silver'),
(3, 'Gamma LLC', 'Bronze'),
(4, 'Delta Health', 'Gold'),
(5, 'Epsilon Retail', 'Bronze');

INSERT INTO products (product_id, product_name, category) VALUES
(101, 'Cloud Server Blade', 'Infrastructure'),
(102, 'Network Switch 48P', 'Networking'),
(103, 'SaaS Annual Seat', 'Software'),
(104, 'Support Ticket Pack', 'Services');

INSERT INTO orders (order_id, customer_id, order_date) VALUES
(5001, 1, '2024-01-15'),
(5002, 1, '2024-02-10'),
(5003, 2, '2024-01-20'),
(5004, 3, '2024-02-12');

INSERT INTO order_items (item_id, order_id, product_id, quantity, unit_price) VALUES
(1, 5001, 101, 2, 1500.00),
(2, 5001, 102, 1, 800.00),
(3, 5002, 103, 5, 250.00),
(4, 5003, 104, 2, 400.00),
(5, 5004, 101, 1, 1500.00);
"""

DATASET_1_10 = """
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
"""

# ==========================================
# UNIT 2 DATASETS
# ==========================================

DATASET_2_1 = """
-- Dataset 2-1: User Transaction Chronology (ROW_NUMBER)
DROP TABLE IF EXISTS user_transactions;

CREATE TABLE user_transactions (
    txn_id VARCHAR(20) PRIMARY KEY,
    user_id INT,
    txn_time TIMESTAMP,
    amount DECIMAL(10, 2)
);

INSERT INTO user_transactions (txn_id, user_id, txn_time, amount) VALUES
('TXN-101', 1, '2024-01-01 08:30:00', 45.00),
('TXN-102', 1, '2024-01-02 09:15:00', 120.00),
('TXN-103', 1, '2024-01-05 14:20:00', 60.00),
('TXN-104', 2, '2024-01-01 11:00:00', 300.00),
('TXN-105', 2, '2024-01-03 16:45:00', 85.00),
('TXN-106', 3, '2024-01-02 10:10:00', 500.00);
"""

DATASET_2_2 = """
-- Dataset 2-2: Monthly Sales Performance (DENSE_RANK)
DROP TABLE IF EXISTS sales_reps;

CREATE TABLE sales_reps (
    rep_id INT PRIMARY KEY,
    rep_name VARCHAR(50),
    region VARCHAR(30),
    closed_revenue DECIMAL(10, 2)
);

INSERT INTO sales_reps (rep_id, rep_name, region, closed_revenue) VALUES
(1, 'Alice Walker', 'North', 150000.00),
(2, 'Bob Stone', 'North', 120000.00),
(3, 'Charlie Hayes', 'North', 150000.00),
(4, 'Diana Prince', 'North', 95000.00),
(5, 'Evan Wright', 'South', 180000.00),
(6, 'Fiona Gallagher', 'South', 180000.00),
(7, 'George Clark', 'South', 130000.00);
"""

DATASET_2_3 = """
-- Dataset 2-3: Daily Server Ingestion Request Volume (LAG)
DROP TABLE IF EXISTS server_metrics;

CREATE TABLE server_metrics (
    metric_date DATE PRIMARY KEY,
    request_count INT,
    error_count INT
);

INSERT INTO server_metrics (metric_date, request_count, error_count) VALUES
('2024-03-01', 12000, 45),
('2024-03-02', 14500, 52),
('2024-03-03', 13800, 39),
('2024-03-04', 18200, 110),
('2024-03-05', 21000, 140),
('2024-03-06', 19500, 95),
('2024-03-07', 22500, 105);
"""

DATASET_2_4 = """
-- Dataset 2-4: User Event Stream and Next Action (LEAD)
DROP TABLE IF EXISTS user_events;

CREATE TABLE user_events (
    event_id INT PRIMARY KEY,
    session_id VARCHAR(30),
    event_time TIMESTAMP,
    page_name VARCHAR(50)
);

INSERT INTO user_events (event_id, session_id, event_time, page_name) VALUES
(1, 'SESS-A', '2024-03-10 10:00:00', 'homepage'),
(2, 'SESS-A', '2024-03-10 10:02:15', 'product_catalog'),
(3, 'SESS-A', '2024-03-10 10:06:40', 'product_detail'),
(4, 'SESS-A', '2024-03-10 10:08:10', 'cart'),
(5, 'SESS-B', '2024-03-10 11:15:00', 'landing_page'),
(6, 'SESS-B', '2024-03-10 11:17:30', 'signup_form'),
(7, 'SESS-B', '2024-03-10 11:19:00', 'dashboard');
"""

DATASET_2_5 = """
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
"""

DATASET_2_6 = """
-- Dataset 2-6: IoT Sensor Temperature Telemetry (Moving Average)
DROP TABLE IF EXISTS sensor_telemetry;

CREATE TABLE sensor_telemetry (
    reading_id INT PRIMARY KEY,
    sensor_id VARCHAR(20),
    reading_day DATE,
    temperature_celsius DECIMAL(5, 2)
);

INSERT INTO sensor_telemetry (reading_id, sensor_id, reading_day, temperature_celsius) VALUES
(1, 'SENSOR-01', '2024-04-01', 22.50),
(2, 'SENSOR-01', '2024-04-02', 23.10),
(3, 'SENSOR-01', '2024-04-03', 25.40),
(4, 'SENSOR-01', '2024-04-04', 24.80),
(5, 'SENSOR-01', '2024-04-05', 28.20),
(6, 'SENSOR-01', '2024-04-06', 29.00),
(7, 'SENSOR-01', '2024-04-07', 26.50),
(8, 'SENSOR-01', '2024-04-08', 23.00),
(9, 'SENSOR-01', '2024-04-09', 22.80),
(10, 'SENSOR-01', '2024-04-10', 21.90);
"""

DATASET_2_7 = """
-- Dataset 2-7: Departmental Compensation Distribution
DROP TABLE IF EXISTS employee_compensation;

CREATE TABLE employee_compensation (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    dept_name VARCHAR(40),
    base_salary DECIMAL(10, 2)
);

INSERT INTO employee_compensation (emp_id, name, dept_name, base_salary) VALUES
(1, 'Alice Cooper', 'Engineering', 130000.00),
(2, 'Bob Martin', 'Engineering', 110000.00),
(3, 'Charlie Daniels', 'Engineering', 150000.00),
(4, 'Diana Ross', 'Finance', 95000.00),
(5, 'Edward Norton', 'Finance', 105000.00),
(6, 'Fiona Apple', 'Marketing', 88000.00),
(7, 'Gordon Ramsay', 'Marketing', 92000.00),
(8, 'Hannah Abbott', 'Marketing', 115000.00);
"""

DATASET_2_8 = """
-- Dataset 2-8: Order Funnel Multi-Step Pipeline (CTE)
DROP TABLE IF EXISTS store_orders;

CREATE TABLE store_orders (
    order_id INT PRIMARY KEY,
    store_id INT,
    order_timestamp TIMESTAMP,
    order_value DECIMAL(10, 2)
);

INSERT INTO store_orders (order_id, store_id, order_timestamp, order_value) VALUES
(1, 101, '2024-02-01 10:15:00', 45.00),
(2, 101, '2024-02-01 14:20:00', 120.00),
(3, 101, '2024-02-02 09:30:00', 310.00),
(4, 102, '2024-02-01 11:00:00', 80.00),
(5, 102, '2024-02-02 16:00:00', 520.00),
(6, 102, '2024-02-02 18:30:00', 140.00),
(7, 103, '2024-02-01 08:45:00', 950.00),
(8, 103, '2024-02-02 12:10:00', 400.00);
"""

DATASET_2_9 = """
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
"""

DATASET_2_10 = """
-- Dataset 2-10: Customer Lifecycle & Purchase Intervals
DROP TABLE IF EXISTS customer_purchases;
DROP TABLE IF EXISTS customer_signups;

CREATE TABLE customer_signups (
    customer_id INT PRIMARY KEY,
    signup_date DATE,
    channel VARCHAR(30)
);

CREATE TABLE customer_purchases (
    purchase_id INT PRIMARY KEY,
    customer_id INT,
    purchase_date DATE,
    amount DECIMAL(10, 2)
);

INSERT INTO customer_signups (customer_id, signup_date, channel) VALUES
(1, '2024-01-01', 'Organic'),
(2, '2024-01-02', 'Paid Search'),
(3, '2024-01-05', 'Referral'),
(4, '2024-01-10', 'Organic');

INSERT INTO customer_purchases (purchase_id, customer_id, purchase_date, amount) VALUES
(101, 1, '2024-01-03', 50.00),
(102, 1, '2024-01-20', 80.00),
(103, 1, '2024-02-15', 120.00),
(104, 2, '2024-01-04', 300.00),
(105, 2, '2024-01-05', 150.00),
(106, 3, '2024-01-12', 45.00);
"""

# ==========================================
# UNIT 3 DATASETS
# ==========================================

DATASET_3_1 = """
-- Dataset 3-1: Dirty User Registration Log
DROP TABLE IF EXISTS raw_leads;

CREATE TABLE raw_leads (
    lead_id INT PRIMARY KEY,
    raw_name VARCHAR(100),
    raw_email VARCHAR(100),
    country VARCHAR(30)
);

INSERT INTO raw_leads (lead_id, raw_name, raw_email, country) VALUES
(1, '   ALEXANDER SMITH  ', 'ALEX@EXAMPLE.COM   ', 'USA'),
(2, 'maria garcia', '   Maria.Garcia@Domain.Org', 'spain'),
(3, '  KEVIN TRAN  ', 'kevin.tran@company.io', 'VIETNAM'),
(4, ' Sarah Connor ', '  SARAH.C@SKY.NET ', 'usa'),
(5, 'david  lee', 'DAVID.LEE@WEBMAIL.COM', 'Canada');
"""

DATASET_3_2 = """
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
"""

DATASET_3_3 = """
-- Dataset 3-3: Duplicate Webhook Events
DROP TABLE IF EXISTS payment_webhooks;

CREATE TABLE payment_webhooks (
    record_id INT PRIMARY KEY,
    event_id VARCHAR(30),
    txn_ref VARCHAR(30),
    amount DECIMAL(10, 2),
    received_at TIMESTAMP
);

INSERT INTO payment_webhooks (record_id, event_id, txn_ref, amount, received_at) VALUES
(1, 'EVT-101', 'TXN-9001', 120.50, '2024-03-01 12:00:01'),
(2, 'EVT-101', 'TXN-9001', 120.50, '2024-03-01 12:00:03'),
(3, 'EVT-102', 'TXN-9002', 85.00, '2024-03-01 12:05:10'),
(4, 'EVT-103', 'TXN-9003', 340.00, '2024-03-01 12:10:00'),
(5, 'EVT-103', 'TXN-9003', 340.00, '2024-03-01 12:10:02');
"""

DATASET_3_4 = """
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
"""

DATASET_3_5 = """
-- Dataset 3-5: Customer Account Health Segmentation
DROP TABLE IF EXISTS customer_activity;

CREATE TABLE customer_activity (
    customer_id INT PRIMARY KEY,
    company_name VARCHAR(50),
    lifetime_spend DECIMAL(10, 2),
    days_since_last_login INT
);

INSERT INTO customer_activity (customer_id, company_name, lifetime_spend, days_since_last_login) VALUES
(1, 'Alpha Tech', 25000.00, 4),
(2, 'Beta Logistics', 4500.00, 45),
(3, 'Gamma Global', 85000.00, 2),
(4, 'Delta Dynamics', 800.00, 120),
(5, 'Epsilon Retail', 12000.00, 18),
(6, 'Zeta Health', 500.00, 5);
"""

DATASET_3_6 = """
-- Dataset 3-6: Transit Turnaround Time with Outlier Skew & Nulls
DROP TABLE IF EXISTS delivery_performance;

CREATE TABLE delivery_performance (
    delivery_id VARCHAR(20) PRIMARY KEY,
    carrier VARCHAR(30),
    transit_days DECIMAL(6, 2)
);

INSERT INTO delivery_performance (delivery_id, carrier, transit_days) VALUES
('DEL-01', 'SpeedyFreight', 2.0),
('DEL-02', 'SpeedyFreight', 3.0),
('DEL-03', 'SpeedyFreight', 2.5),
('DEL-04', 'SpeedyFreight', NULL),
('DEL-05', 'SpeedyFreight', 19.0),
('DEL-06', 'SpeedyFreight', 3.0),
('DEL-07', 'SpeedyFreight', NULL),
('DEL-08', 'SpeedyFreight', 2.8);
"""

DATASET_3_7 = """
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
"""

DATASET_3_8 = """
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
"""

DATASET_3_9 = """
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
"""

DATASET_3_10 = """
-- Dataset 3-10: IoT Pressure Telemetry with Noise Outliers
DROP TABLE IF EXISTS iot_factory_readings;

CREATE TABLE iot_factory_readings (
    reading_id INT PRIMARY KEY,
    device_id VARCHAR(20),
    reading_timestamp TIMESTAMP,
    pressure_psi DECIMAL(6, 2)
);

INSERT INTO iot_factory_readings (reading_id, device_id, reading_timestamp, pressure_psi) VALUES
(1, 'PUMP-A', '2024-05-01 08:00:00', 45.2),
(2, 'PUMP-A', '2024-05-01 08:05:00', 46.0),
(3, 'PUMP-A', '2024-05-01 08:10:00', 45.8),
(4, 'PUMP-A', '2024-05-01 08:15:00', 198.5),
(5, 'PUMP-A', '2024-05-01 08:20:00', 46.1),
(6, 'PUMP-A', '2024-05-01 08:25:00', 45.5),
(7, 'PUMP-B', '2024-05-01 08:00:00', 60.1),
(8, 'PUMP-B', '2024-05-01 08:05:00', 59.8),
(9, 'PUMP-B', '2024-05-01 08:10:00', NULL),
(10, 'PUMP-B', '2024-05-01 08:15:00', 60.5);
"""

DATASETS = {
    # Unit 1
    "dataset1-1-easy-inner-join-sales.sql": DATASET_1_1,
    "dataset1-2-easy-left-join-nulls.sql": DATASET_1_2,
    "dataset1-3-easy-basic-aggregations.sql": DATASET_1_3,
    "dataset1-4-easy-group-by-having-filter.sql": DATASET_1_4,
    "dataset1-5-medium-multi-table-inventory.sql": DATASET_1_5,
    "dataset1-6-medium-full-outer-discrepancy.sql": DATASET_1_6,
    "dataset1-7-medium-union-all-log-stacking.sql": DATASET_1_7,
    "dataset1-8-medium-conditional-aggregations.sql": DATASET_1_8,
    "dataset1-9-hard-multi-tier-customer-spend.sql": DATASET_1_9,
    "dataset1-10-hard-normalized-inventory-reconciliation.sql": DATASET_1_10,
    
    # Unit 2
    "dataset2-1-easy-row-number-ranking.sql": DATASET_2_1,
    "dataset2-2-easy-dense-rank-leaderboard.sql": DATASET_2_2,
    "dataset2-3-easy-lag-period-comparison.sql": DATASET_2_3,
    "dataset2-4-easy-lead-forward-tracking.sql": DATASET_2_4,
    "dataset2-5-medium-running-cumulative-revenue.sql": DATASET_2_5,
    "dataset2-6-medium-rolling-moving-average.sql": DATASET_2_6,
    "dataset2-7-medium-partitioned-window-stats.sql": DATASET_2_7,
    "dataset2-8-medium-cte-sequential-pipeline.sql": DATASET_2_8,
    "dataset2-9-hard-weighted-moving-avg-sympy.sql": DATASET_2_9,
    "dataset2-10-hard-retention-cohort-progression.sql": DATASET_2_10,

    # Unit 3
    "dataset3-1-easy-text-trim-casing.sql": DATASET_3_1,
    "dataset3-2-easy-null-coalesce-imputation.sql": DATASET_3_2,
    "dataset3-3-easy-row-deduplication.sql": DATASET_3_3,
    "dataset3-4-easy-type-casting-dates.sql": DATASET_3_4,
    "dataset3-5-medium-conditional-case-when.sql": DATASET_3_5,
    "dataset3-6-medium-median-imputation-pandas.sql": DATASET_3_6,
    "dataset3-7-medium-duckdb-virtual-view-ingestion.sql": DATASET_3_7,
    "dataset3-8-medium-idempotent-table-creation.sql": DATASET_3_8,
    "dataset3-9-hard-dirty-etl-pipeline-duckdb.sql": DATASET_3_9,
    "dataset3-10-hard-anomaly-audit-ingestion.sql": DATASET_3_10,
}

def main():
    os.makedirs(SQL_DIR, exist_ok=True)
    for filename, content in DATASETS.items():
        write_sql(filename, content)
    print(f"Successfully generated all {len(DATASETS)} datasets in {SQL_DIR}")

if __name__ == "__main__":
    main()
