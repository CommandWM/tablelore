# Security Policy

TableLore is designed for local-first analysis. It should not upload private datasets or send raw records to external services unless a user explicitly approves that path.

## Reporting a Vulnerability

Open a private security advisory on GitHub if available, or contact the repository owner directly. Avoid posting private data, credentials, proprietary schemas, or sensitive row-level examples in public issues.

## Data Handling Expectations

- Prefer schemas, aggregates, and safe samples over raw data dumps.
- Keep committed examples synthetic.
- Do not add credentials, real customer data, or private extracts to dogfood fixtures.
- Treat leakage-prone columns, notes, identifiers, and post-outcome fields conservatively.
