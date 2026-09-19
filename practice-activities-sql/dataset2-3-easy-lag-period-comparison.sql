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
