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
