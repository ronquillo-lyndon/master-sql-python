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
