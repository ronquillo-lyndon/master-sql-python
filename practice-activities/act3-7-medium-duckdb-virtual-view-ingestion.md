# Activity 3-7 (Medium): Zero-Copy DuckDB Virtual View Ingestion

## Problem Scenario
Data analysts need to run high-speed OLAP queries on a cleaned vendor catalog DataFrame stored in Python memory (`supplier_catalog`). Rather than exporting to disk or spinning up a full PostgreSQL server, the pipeline utilizes **DuckDB**. 

Demonstrate an in-process data engineering pattern:
1. Register a Pandas DataFrame as a temporary virtual view inside an in-memory DuckDB connection (`conn.register()`).
2. Execute an analytical SQL aggregation query directly against the registered virtual view to calculate:
   - Total catalog SKUs per `brand`
   - Average wholesale price per `brand`
   - Total warehouse asset valuation per `brand` (`wholesale_price * available_stock`)
3. Persist the aggregated results directly into a physical DuckDB table `brand_valuation_summary`.
4. Fetch the resulting table back into Pandas via `.fetchdf()`.

### Data Schema Overview
- **`supplier_catalog` DataFrame**: `sku` (VARCHAR), `brand` (VARCHAR), `wholesale_price` (DECIMAL), `available_stock` (INT)

### Objectives
1. Connect to DuckDB (`duckdb.connect()`).
2. Register DataFrame as a virtual view.
3. Run DDL `CREATE TABLE AS SELECT ...` aggregating metrics.
4. Retrieve results using `.fetchdf()`.

## Hints
- `duckdb.connect(':memory:')` provides an ultra-fast, local in-process analytical engine.
- `conn.register('view_name', df)` makes Python DataFrames directly queryable from standard SQL without copying memory.
