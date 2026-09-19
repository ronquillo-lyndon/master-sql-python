# Activity 3-8 (Medium): Building Idempotent Ingestion Pipelines

## Problem Scenario
In production data engineering, pipelines are scheduled to run on recurring schedules (e.g. hourly or daily). If an orchestrator triggers a retry due to a transient network hiccup, a non-idempotent ingestion script will crash because tables already exist, or worse, append duplicate records into the analytical data warehouse. 

Build an **idempotent** ingestion script that processes staging records from `daily_ledger_staging`. The pipeline must:
1. Ensure table schema creation executes safely regardless of how many times the script is rerun (`CREATE TABLE IF NOT EXISTS`).
2. Guarantee that successive executions replace or update the staging partition cleanly rather than accumulating duplicate records.
3. Validate final table row counts and integrity.

### Data Schema Overview
- **`daily_ledger_staging` Table**: `entry_id` (INT), `account_code` (VARCHAR), `entry_date` (DATE), `amount` (DECIMAL)

### Objectives
1. Use idempotent SQL statements (`CREATE TABLE IF NOT EXISTS`, atomic replacement or upsert).
2. Test running the ingestion script twice in succession to prove idempotency.
3. Verify that the destination table contains the exact expected record count after both runs.

## Hints
- A pipeline is idempotent if $f(f(x)) = f(x)$—running it multiple times produces the exact same end state.
- In DuckDB / SQL, `CREATE OR REPLACE TABLE` or `CREATE TABLE IF NOT EXISTS` combined with partition clearing ensures idempotency.
