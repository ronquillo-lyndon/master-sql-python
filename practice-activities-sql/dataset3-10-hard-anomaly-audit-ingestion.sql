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
