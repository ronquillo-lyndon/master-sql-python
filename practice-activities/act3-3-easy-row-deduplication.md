# Activity 3-3 (Easy): Payment Webhook Deduplication Pipeline

## Problem Scenario
Payment gateway webhooks stream real-time settlement notices into `payment_webhooks`. Due to network retries, duplicate delivery attempts frequently insert multiple identical event notifications with the same `event_id` and transaction reference `txn_ref`, but differing `record_id` and slight timestamp variances. 

The accounting pipeline must filter out all duplicate webhook delivery attempts, retaining strictly the **first** received event per `event_id`.

### Data Schema Overview
- **`payment_webhooks` Table**: `record_id` (INT), `event_id` (VARCHAR), `txn_ref` (VARCHAR), `amount` (DECIMAL), `received_at` (TIMESTAMP)

### Objectives
1. Identify records that share identical `event_id` keys.
2. In SQL, use `ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY received_at ASC)` inside a CTE or subquery and filter for `row_num = 1`.
3. In Python, apply `.drop_duplicates(subset=['event_id'], keep='first')`.
4. Order the clean output by `record_id` ascending.

## Hints
- When duplicate rows differ by a metadata field (such as `received_at` or auto-incrementing ID), standard `SELECT DISTINCT *` fails. Instead, use partitioned ranking or dedicated deduplication methods.
- In Pandas, `.drop_duplicates()` with `keep='first'` requires the DataFrame to be pre-sorted by the desired timestamp order.
