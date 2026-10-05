# Product Requirements

## Product

A private, read-only-first investment manager for long-term household planning. It records dated financial evidence, calculates deterministic portfolio and cash-flow analysis, and produces sourced Markdown reports for human decisions.

## Users

- Primary: household owner and decision maker.
- Secondary: spouse, where ownership and authorization are explicit.
- Operator: the same household user running a manual Docker deployment.

## Goals

- Preserve ownership, account, source, currency, valuation date, and provenance.
- Import dated snapshots idempotently without double counting.
- Reconcile one complete statement period before broad analysis.
- Calculate allocation, cash flows, scenarios, and retirement projections in Python.
- Use an LLM only for sourced explanation and research.
- Produce auditable reports and decision records.
- Recover the application on another computer from Git and private backups.

## Non-goals

- Autonomous trading, broker order submission, liquidation, or rebalancing.
- Treating planned asset sales as available cash.
- Replacing bank statements, ERPNext, or broker records as the system of record.
- Inferring missing balances, expenses, ownership, or goals.
- Providing guaranteed returns, drawdown ceilings, or sustainable withdrawal rates.
- Copying private household records into the public repository.

## Functional requirements

1. Accept validated dated source records with stable source identity.
2. Reject malformed dates, currencies, identifiers, and non-finite money values.
3. Preserve corrections and failed-import status; never convert failure to zero.
4. Keep deposits, withdrawals, transfers, expenses, and investment returns distinct.
5. Preserve separate owners and accounts even when instruments share a ticker.
6. Produce deterministic calculation output independently of LLM availability.
7. Mark stale, missing, conflicting, and unverified evidence in reports.
8. Require explicit user authorization for policy changes or financial transactions.
9. Keep external documents and LLM output untrusted and non-executable.
10. Provide a reproducible Docker run and documented backup/restore procedure.

## Initial acceptance criteria

- Synthetic snapshot checks pass natively and in Docker.
- Repeating the same import leaves totals unchanged.
- An invalid import fails without changing stored data.
- Ownership totals reconcile to household totals for a valid snapshot.
- A missing LLM memo leaves numeric results available and clearly marked.
- Reports include source references and as-of dates.
- No public test fixture contains real household balances or account identifiers.

## Success measures

- Every reported number has a source, date, and classification.
- No duplicate capital from repeated imports.
- No unauthorized write to Drive, ERPNext, or a broker.
- A clean-machine recovery test can restore the latest verified state.

## Constraints

Python standard library and SQLite are preferred. The current milestone is manual, reporting-only, and Markdown-first. Private data belongs in ignored local paths or private services.
