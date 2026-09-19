# Solution 3-4 (Easy): Type Ingestion: Parsing Untyped Raw Invoices

## SQL Implementation
```sql
SELECT 
    invoice_id,
    -- Reason: Cast string date to native SQL DATE for proper temporal ordering and indexing
    CAST(string_date AS DATE) AS invoice_date,
    -- Reason: Cast string amount to numerical DECIMAL for accurate arithmetic
    CAST(raw_amount_str AS DECIMAL(10, 2)) AS amount,
    -- Reason: Compute derived tax calculation on properly typed numerical column
    ROUND(CAST(raw_amount_str AS DECIMAL(10, 2)) * 0.08, 2) AS sales_tax
FROM raw_staging_invoices
ORDER BY invoice_date ASC;
```

## Python Implementation
```python
import pandas as pd

raw_staging_invoices = pd.DataFrame({
    'invoice_id': ['INV-801', 'INV-802', 'INV-803', 'INV-804', 'INV-805'],
    'string_date': ['2024-01-15', '2024-01-16', '2024-01-20', '2024-01-22', '2024-01-25'],
    'raw_amount_str': ['1450.50', '320.00', '890.75', '1100.00', '45.25']
})

# Reason: Parse string dates to datetime64 type
raw_staging_invoices['invoice_date'] = pd.to_datetime(raw_staging_invoices['string_date'])

# Reason: Cast string numbers to float64 for mathematical operations
raw_staging_invoices['amount'] = raw_staging_invoices['raw_amount_str'].astype(float)

# Reason: Vectorized calculation of derived tax metric
raw_staging_invoices['sales_tax'] = (raw_staging_invoices['amount'] * 0.08).round(2)

result_df = raw_staging_invoices[['invoice_id', 'invoice_date', 'amount', 'sales_tax']].sort_values(by='invoice_date')
print(result_df)
```
