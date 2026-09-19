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
