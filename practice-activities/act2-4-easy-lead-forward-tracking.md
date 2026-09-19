# Activity 2-4 (Easy): Tracking Next User Action with LEAD

## Problem Scenario
A product analytics team is studying web conversion funnels recorded in a `user_events` table. To understand navigational flow within each user session (`session_id`), the team needs to know the subsequent page visited (`next_page`) and the timestamp of that subsequent event. If the event is the terminal action of the session, `next_page` should display `'SESSION_END'`.

### Data Schema Overview
- **`user_events` Table**: `event_id` (INT), `session_id` (VARCHAR), `event_time` (TIMESTAMP), `page_name` (VARCHAR)

### Objectives
1. Partition the events by `session_id`.
2. Order events chronologically by `event_time`.
3. Use `LEAD` to project the next visited `page_name`.
4. Replace NULL in terminal events with `'SESSION_END'`.
5. Order output by `session_id`, then `event_time`.

## Hints
- `LEAD` looks forward into future rows within the defined window frame.
- Specify a default fallback value in `LEAD` to handle the final row in each partition gracefully.
- In Pandas, `.shift(-1)` shifts rows upward to look forward into the subsequent record.
