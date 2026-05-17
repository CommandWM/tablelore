## Summary

-

## Checks

- [ ] `python3 -m pytest tests -q`
- [ ] `python3 tablelore/scripts/table_profile.py tests/fixtures/customer_churn_sample.csv --target churned`
- [ ] `python3 dogfood/com47/run_dogfood.py`

## Scope

- [ ] Skill guidance remains local-first.
- [ ] No AutoML, hosted service, or full CLI packaging added unless explicitly scoped.
- [ ] Private/raw data is not included in examples or artifacts.
