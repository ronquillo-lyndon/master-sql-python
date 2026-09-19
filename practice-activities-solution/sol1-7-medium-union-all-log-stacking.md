# Solution 1-7 (Medium): Unifying Web and Mobile Event Streams

## SQL Implementation
```sql
-- Query 1: Extract web events with literal platform tag
SELECT 
    event_id,
    user_id,
    'WEB' AS platform,
    action_type,
    event_timestamp
FROM web_clicks

UNION ALL

-- Reason: UNION ALL concatenates rows directly without performing an expensive distinct sort
-- Query 2: Extract mobile events with literal platform tag
SELECT 
    event_id,
    user_id,
    'MOBILE' AS platform,
    action_type,
    event_timestamp
FROM mobile_taps

-- Reason: Sort combined event stream chronologically
ORDER BY event_timestamp ASC;
```

## Python Implementation
```python
import pandas as pd

web_clicks = pd.DataFrame({
    'event_id': ['WEB-01', 'WEB-02', 'WEB-03', 'WEB-04'],
    'user_id': [101, 102, 101, 103],
    'action_type': ['page_view', 'add_to_cart', 'checkout_start', 'page_view'],
    'event_timestamp': ['2024-03-01 10:01:05', '2024-03-01 10:05:12', '2024-03-01 10:12:44', '2024-03-01 10:15:30']
})

mobile_taps = pd.DataFrame({
    'event_id': ['MOB-01', 'MOB-02', 'MOB-03', 'MOB-04'],
    'user_id': [102, 104, 101, 102],
    'action_type': ['app_open', 'page_view', 'push_dismiss', 'checkout_success'],
    'event_timestamp': ['2024-03-01 10:00:20', '2024-03-01 10:04:15', '2024-03-01 10:11:00', '2024-03-01 10:20:00']
})

# Reason: Assign literal platform tags to match SQL query structure
web_clicks['platform'] = 'WEB'
mobile_taps['platform'] = 'MOBILE'

# Reason: pd.concat with axis=0 performs SQL UNION ALL equivalent
unified_events = pd.concat([web_clicks, mobile_taps], axis=0, ignore_index=True)

# Reason: Sort chronologically across the unified platform timeline
unified_events = unified_events.sort_values(by='event_timestamp', ascending=True)

print(unified_events)
```
