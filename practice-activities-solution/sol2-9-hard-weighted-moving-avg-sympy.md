# Solution 2-9 (Hard): Symbolic Formula Derivation & Weighted Moving Average

## Python Implementation (SymPy Derivation + Vectorized Pandas)
```python
import sympy as sp
import pandas as pd
import numpy as np

# ==========================================
# 1. SymPy Step: Symbolic Formula Verification
# ==========================================
# Reason: Algebraically verify weight distribution before deploying to pipeline
p0, p1, p2 = sp.symbols('p0 p1 p2') # p0 = current, p1 = lag1, p2 = lag2
w0, w1, w2 = sp.symbols('w0 w1 w2')

formula = (p0 * w0 + p1 * w1 + p2 * w2) / (w0 + w1 + w2)
verified_formula = formula.subs({w0: 0.5, w1: 0.3, w2: 0.2})
print(f"Verified Symbolic Formula: {verified_formula}")

# ==========================================
# 2. Vectorized Pandas Execution
# ==========================================
stock_price_history = pd.DataFrame({
    'trade_date': ['2024-03-01', '2024-03-04', '2024-03-05', '2024-03-06', '2024-03-07', '2024-03-08', '2024-03-11', '2024-03-12'],
    'ticker': ['ACME'] * 8,
    'close_price': [100.00, 105.00, 102.50, 110.00, 108.00, 115.00, 118.50, 114.00]
})

stock_price_history['trade_date'] = pd.to_datetime(stock_price_history['trade_date'])
stock_price_history = stock_price_history.sort_values(by='trade_date').reset_index(drop=True)

# Reason: Use .shift() to obtain lag1 and lag2
stock_price_history['lag1'] = stock_price_history['close_price'].shift(1)
stock_price_history['lag2'] = stock_price_history['close_price'].shift(2)

# Reason: Implement symbolically verified formula
stock_price_history['weighted_moving_avg'] = (
    0.5 * stock_price_history['close_price'] + 
    0.3 * stock_price_history['lag1'] + 
    0.2 * stock_price_history['lag2']
).round(2)

print(stock_price_history[['trade_date', 'ticker', 'close_price', 'weighted_moving_avg']])
```

## SQL Implementation
```sql
WITH lagged_prices AS (
    SELECT 
        trade_date,
        ticker,
        close_price,
        -- Reason: LAG accesses prior prices at offset 1 and offset 2
        LAG(close_price, 1) OVER (ORDER BY trade_date ASC) AS lag1,
        LAG(close_price, 2) OVER (ORDER BY trade_date ASC) AS lag2
    FROM stock_price_history
)
SELECT 
    trade_date,
    ticker,
    close_price,
    -- Reason: If lag2 is NULL, less than 3 days of historical data exist; return NULL
    CASE 
        WHEN lag2 IS NOT NULL THEN 
            ROUND((0.5 * close_price) + (0.3 * lag1) + (0.2 * lag2), 2)
        ELSE NULL 
    END AS weighted_moving_avg
FROM lagged_prices
ORDER BY trade_date ASC;
```
