# Activity 2-9 (Hard): Symbolic Formula Derivation & Weighted Moving Average

## Problem Scenario
A quantitative trading desk analyses daily equity closing prices recorded in `stock_price_history`. Quantitative analysts want to smooth price volatility using a 3-day exponentially decaying weighted moving average where:
- Day $t$ (today) receives weight $w_3 = 0.5$
- Day $t-1$ (yesterday) receives weight $w_2 = 0.3$
- Day $t-2$ (two days ago) receives weight $w_1 = 0.2$

The analytical engineering workflow requires:
1. **Symbolic Derivation**: Use SymPy to algebraically formulate the weighted average equation, simplify it, and verify that the weights sum to 1.0.
2. **SQL & Programmatic Implementation**: Use analytical window functions (`LAG`) in SQL and vectorized `.shift()` in Pandas to calculate the weighted moving average across the time series. For the first two trading dates (where 3 full days of history do not exist), output `NULL` or `NaN`.

### Data Schema Overview
- **`stock_price_history` Table**: `trade_date` (DATE), `ticker` (VARCHAR), `close_price` (DECIMAL)

### Objectives
1. Define algebraic symbols in SymPy and substitute weight values.
2. Implement lag window functions to extract historical prices at offsets 1 and 2.
3. Compute `weighted_moving_avg = (0.5 * close_price) + (0.3 * lag1) + (0.2 * lag2)`.
4. Order output by `trade_date` ascending.

## Hints
- In SymPy, define symbols with `sp.symbols('p0 p1 p2 w1 w2 w3')` and compute the weighted expression divided by the sum of weights.
- In SQL, `LAG(close_price, 1)` and `LAG(close_price, 2)` retrieve prior day values. A `CASE WHEN` can suppress rows without 2 preceding trading days.
