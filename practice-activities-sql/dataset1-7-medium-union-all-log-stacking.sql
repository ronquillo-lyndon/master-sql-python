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
