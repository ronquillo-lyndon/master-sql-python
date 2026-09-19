# Solution 3-1 (Easy): Ingestion Cleansing of Dirty User Strings

## SQL Implementation
```sql
SELECT 
    lead_id,
    -- Reason: TRIM removes accidental leading and trailing whitespace.
    -- (In standard SQL, UPPER/LOWER handles casing; database extensions or Python handle title-casing).
    TRIM(raw_name) AS cleaned_name,
    -- Reason: Lowercase emails to prevent duplicate account lookup errors
    TRIM(LOWER(raw_email)) AS cleaned_email,
    -- Reason: Standardize country to uniform uppercase format (e.g. 'USA')
    TRIM(UPPER(country)) AS standardized_country
FROM raw_leads
ORDER BY lead_id ASC;
```

## Python Implementation
```python
import pandas as pd

raw_leads = pd.DataFrame({
    'lead_id': [1, 2, 3, 4, 5],
    'raw_name': ['   ALEXANDER SMITH  ', 'maria garcia', '  KEVIN TRAN  ', ' Sarah Connor ', 'david  lee'],
    'raw_email': ['ALEX@EXAMPLE.COM   ', '   Maria.Garcia@Domain.Org', 'kevin.tran@company.io', '  SARAH.C@SKY.NET ', 'DAVID.LEE@WEBMAIL.COM'],
    'country': ['USA', 'spain', 'VIETNAM', 'usa', 'Canada']
})

# Reason: Replicate programmatic pre-processing using Lambda and vectorized string functions
# 1. Clean and Title-Case customer names
raw_leads['cleaned_name'] = raw_leads['raw_name'].apply(lambda x: str(x).strip().title())

# 2. Strip whitespace and lowercase emails
raw_leads['cleaned_email'] = raw_leads['raw_email'].apply(lambda x: str(x).strip().lower())

# 3. Strip whitespace and uppercase country names
raw_leads['standardized_country'] = raw_leads['country'].apply(lambda x: str(x).strip().upper())

result_df = raw_leads[['lead_id', 'cleaned_name', 'cleaned_email', 'standardized_country']].sort_values(by='lead_id')
print(result_df)
```
