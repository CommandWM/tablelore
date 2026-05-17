# Leakage Check

Question: check `support_tickets.csv` for leakage before training a churn model.

Modeling readiness:
- Target: `churned_30d`, positive class `1`.
- Observation grain: one row appears to represent one support ticket, but duplicate `ticket_id` values show the grain is not clean.
- Label distribution: {1: 4, 0: 2}.
- Prediction time: ticket open time; features should be available at or shortly after `opened_at`.

Leakage candidates:
- `resolution_status`: contains post-ticket outcomes such as cancellation/refund-style states.
- `post_churn_note`: explicitly contains post-outcome text and should be excluded from training.
- Duplicate `ticket_id` values can place the same entity in train and test unless removed or grouped.

Split strategy:
- Use a time-based split by `opened_at` for future prediction, or a grouped split by `account_id` if multiple tickets per account are retained.

Baseline:
- Start with the majority-class or simple severity/response-time rule before advanced models.

Decision:
- Not ready for modeling until duplicate ticket handling, leakage-column exclusion, and split strategy are documented.
