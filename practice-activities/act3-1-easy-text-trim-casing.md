# Activity 3-1 (Easy): Ingestion Cleansing of Dirty User Strings

## Problem Scenario
A customer onboarding intake form writes raw, unvalidated entries directly into a `raw_leads` staging table. Marketing analysts report that leading and trailing whitespace, inconsistent casing in email addresses, and unstandardized country codes are breaking downstream email automation campaigns. 

The data engineering pipeline must clean this raw table by:
1. Stripping all leading and trailing whitespace from names and email addresses.
2. Converting all email addresses to lowercase.
3. Standardizing all country names to uppercase.
4. Converting customer names to title case (capitalizing the first letter of each word).

### Data Schema Overview
- **`raw_leads` Table**: `lead_id` (INT), `raw_name` (VARCHAR), `raw_email` (VARCHAR), `country` (VARCHAR)

### Objectives
1. Use SQL string formatting functions (`TRIM`, `LOWER`, `UPPER`).
2. In Python, use vectorized or lambda string transformations (`.strip()`, `.lower()`, `.title()`).
3. Output `lead_id`, `cleaned_name`, `cleaned_email`, and `standardized_country`.
4. Order by `lead_id` ascending.

## Hints
- SQL provides standard string functions like `TRIM()`, `LOWER()`, and `UPPER()`. Title casing can be handled with built-in functions or application-layer Python lambdas.
- In Python, apply string methods across DataFrame columns using `.str.strip()`, `.str.lower()`, or `.apply(lambda x: ...)`.
