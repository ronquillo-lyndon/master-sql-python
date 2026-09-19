# Activity 1-6 (Medium): Discrepancy Audit with Full Outer Join

## Problem Scenario
During a post-migration audit between an on-premise ERP system and a cloud-based Warehouse Management System (WMS), discrepancies have appeared in logistics billing. The ERP stores outbound shipments in `legacy_shipments`, while the WMS records billed carrier receipts in `platform_receipts`. The financial auditor needs a reconciliation audit report showing every tracking number present in either or both systems, along with the ERP cost, the platform billed amount, and an audit status classifying whether the record is 'Matched', 'Missing in Platform', or 'Missing in Legacy'.

### Data Schema Overview
- **`legacy_shipments` Table**: `tracking_number` (VARCHAR), `erp_cost` (DECIMAL), `shipper_name` (VARCHAR)
- **`platform_receipts` Table**: `tracking_number` (VARCHAR), `billed_amount` (DECIMAL), `carrier_status` (VARCHAR)

### Objectives
1. Perform a full outer join ($A \cup B$) to capture tracking numbers from both systems.
2. Align tracking numbers using `COALESCE`.
3. Categorize the audit status:
   - 'Matched' if present in both.
   - 'Missing in Platform' if only in legacy.
   - 'Missing in Legacy' if only in platform receipts.
4. Order by tracking number ascending.

## Hints
- A full outer join preserves unmatched rows from both sides, producing NULL values whenever a key exists in one table but not the other.
- Use `CASE WHEN` in SQL and `np.select` (or conditional lambda/masking) in Python to assign the audit status based on NULL checks.
