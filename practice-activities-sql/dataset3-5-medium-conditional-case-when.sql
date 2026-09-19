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
