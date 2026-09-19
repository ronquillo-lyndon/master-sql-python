# Solution 2-4 (Easy): Tracking Next User Action with LEAD

## SQL Implementation
```sql
SELECT 
    event_id,
    session_id,
    event_time,
    page_name AS current_page,
    -- Reason: LEAD looks ahead 1 row within each session. Default value 'SESSION_END' handles the last event.
    LEAD(page_name, 1, 'SESSION_END') OVER (
        PARTITION BY session_id 
        ORDER BY event_time ASC
    ) AS next_page
FROM user_events
ORDER BY session_id ASC, event_time ASC;
```

## Python Implementation
```python
import pandas as pd

user_events = pd.DataFrame({
    'event_id': [1, 2, 3, 4, 5, 6, 7],
    'session_id': ['SESS-A', 'SESS-A', 'SESS-A', 'SESS-A', 'SESS-B', 'SESS-B', 'SESS-B'],
    'event_time': ['2024-03-10 10:00:00', '2024-03-10 10:02:15', '2024-03-10 10:06:40', '2024-03-10 10:08:10', '2024-03-10 11:15:00', '2024-03-10 11:17:30', '2024-03-10 11:19:00'],
    'page_name': ['homepage', 'product_catalog', 'product_detail', 'cart', 'landing_page', 'signup_form', 'dashboard']
})

user_events['event_time'] = pd.to_datetime(user_events['event_time'])
user_events = user_events.sort_values(by=['session_id', 'event_time']).reset_index(drop=True)

# Reason: Replicate SQL LEAD using .groupby('session_id')['page_name'].shift(-1)
user_events['next_page'] = user_events.groupby('session_id')['page_name'].shift(-1)

# Reason: Fill missing trailing event with designated literal string
user_events['next_page'] = user_events['next_page'].fillna('SESSION_END')

print(user_events[['session_id', 'event_time', 'page_name', 'next_page']])
```
