# Table Profile

Input: `/Users/matthewdavis/Documents/GitHub/tablelore/dogfood/com47/data/support_tickets.csv`
Format: CSV
File size: 575 bytes
Rows: 6
Columns: 10

## Schema

| column | dtype | missing | missing_pct | distinct |
| --- | --- | --- | --- | --- |
| ticket_id | object | 0 | 0.0% | 5 |
| account_id | object | 0 | 0.0% | 5 |
| opened_at | object | 0 | 0.0% | 5 |
| plan | object | 0 | 0.0% | 3 |
| severity | object | 0 | 0.0% | 4 |
| first_response_hours | float64 | 1 | 16.7% | 4 |
| csat_score | float64 | 2 | 33.3% | 4 |
| churned_30d | int64 | 0 | 0.0% | 2 |
| resolution_status | object | 0 | 0.0% | 3 |
| post_churn_note | object | 2 | 33.3% | 3 |

## Numeric Summary

| column | min | median | mean | max |
| --- | --- | --- | --- | --- |
| first_response_hours | -1 | 8.5 | 17.1 | 48 |
| csat_score | 1 | 3 | 3 | 5 |
| churned_30d | 0 | 1 | 0.6667 | 1 |

## Date Ranges

| column | valid_values | min | max |
| --- | --- | --- | --- |
| opened_at | 6 | 2026-01-03 | 2026-02-12 |

## Category Top Values

| column | distinct | top_values |
| --- | --- | --- |
| plan | 3 | pro: 3, starter: 2, enterprise: 1 |
| severity | 4 | critical: 3, low: 1, high: 1 |
| resolution_status | 3 | canceled_after_ticket: 3, resolved: 2, refund_processed: 1 |

## Keys and Duplicates

Duplicate rows: 1
Candidate key: none found

## Target distribution: churned_30d

| value | count | pct |
| --- | --- | --- |
| 1 | 4 | 66.7% |
| 0 | 2 | 33.3% |

## Warnings

- Missing values found in: first_response_hours, csat_score, post_churn_note.
- Duplicate rows: 1.
- first_response_hours has 2 negative values.
- No single-column candidate key found.
- Potential leakage candidates: resolution_status, post_churn_note.

## Recommended Next Step

Review the warnings and confirm the row grain, candidate keys, target definition, and split strategy before modeling or heavy transformation.
