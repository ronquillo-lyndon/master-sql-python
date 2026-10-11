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

SELECT 
    metric_date,
    request_count,
    error_count,
    LAG(
    request_count, 1, request_count
    ) OVER (ORDER BY metric_date ASC) as prev_request_count,
    request_count - LAG(
        request_count, 1, request_count
    ) OVER (ORDER BY metric_date ASC) as day_over_day_delta
FROM
    server_metrics
ORDER BY metric_date ASC;
