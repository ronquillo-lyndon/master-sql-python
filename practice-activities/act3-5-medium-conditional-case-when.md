# Activity 3-5 (Medium): Customer Retention Segmentation with CASE WHEN

## Problem Scenario
The customer success team uses `customer_activity` to monitor user health. Analysts need to assign every customer to an actionable engagement tier based on business logic:
- **`VIP Active`**: `lifetime_spend >= 20000.00` AND `days_since_last_login <= 30`
- **`VIP Churn Risk`**: `lifetime_spend >= 20000.00` AND `days_since_last_login > 30`
- **`Standard Active`**: `lifetime_spend < 20000.00` AND `days_since_last_login <= 30`
- **`Standard Dormant`**: `lifetime_spend < 20000.00` AND `days_since_last_login > 30`

The report must output each customer, their current metrics, and their evaluated `account_health_tier`.

### Data Schema Overview
- **`customer_activity` Table**: `customer_id` (INT), `company_name` (VARCHAR), `lifetime_spend` (DECIMAL), `days_since_last_login` (INT)

### Objectives
1. Implement multi-branch conditional classification logic using `CASE WHEN ... THEN ... ELSE ... END`.
2. In Python, implement vectorized condition evaluation using `np.select`.
3. Order the resulting report by `lifetime_spend` descending.

## Hints
- `CASE WHEN` evaluates conditions sequentially from top to bottom; the first true branch is returned.
- In Python, `np.select(conditions, choices, default=...)` provides a clean, vectorized equivalent to SQL `CASE WHEN`.
