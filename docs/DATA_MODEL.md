# Data Model

The model must preserve evidence rather than overwrite it. Names below describe the target model; only the portfolio snapshot value object exists today.

## Core entities

### Source

- `source_id`: stable internal identifier.
- `kind`: statement, spreadsheet, receipt, ERPNext export, broker report, or research document.
- `provider`: source system name.
- `external_id`: Drive file ID, ERPNext identifier, or provider reference.
- `uri`: private location when needed; do not expose credentials.
- `period_start`, `period_end`: source coverage dates.
- `retrieved_at`, `checksum`, `status`: provenance and extraction state.

### Account

- `account_id`: stable internal identifier.
- `owner_id`: legal owner or household entity.
- `institution`, `account_type`, `currency`.
- `external_id`: encrypted or redacted outside private storage.
- `status`: active, closed, or unknown.

### Holding snapshot

- `snapshot_id`, `account_id`, `owner_id`.
- `instrument_id`, `product_type`, `platform`.
- `quantity` and `unit_price` when confirmed.
- `value`, `currency`, `valuation_at`, `imported_at`.
- `source_id`, `source_row_id`, `confidence`.

A ticker is not an identity. The account, owner, product, and source row remain part of the identity.

### Cash transaction

- `transaction_id`, `account_id`, `owner_id`, `source_id`, `source_row_id`.
- `posted_at`, `amount`, `currency`, `direction`.
- `classification`: deposit, withdrawal, transfer, expense, income, fee, debt payment, investment purchase/sale, refund, or unknown.
- `counterparty_account_id` for confirmed transfers.
- `status`, `correction_of`, `notes`.

### Policy and decision

- `policy_id`, effective date, author, assumptions, approval status.
- `decision_id`, report ID, reviewer, decision, authorization timestamp, and scope.

## Invariants

- Money is finite and non-negative at field boundaries unless a signed amount is explicitly required.
- Every balance and transaction has a currency and date.
- Every imported row has source and row identity.
- Re-importing the same source row is idempotent.
- Corrections append history rather than erase the prior observation.
- Owners and accounts cannot be inferred from instrument names.
- Failed extraction is a failed record, not a zero balance.
- Transfers do not become household expenses or investment returns.
- Snapshot totals are not performance without dated flow data.

## Privacy

Public fixtures use synthetic IDs and values. Real source IDs, account numbers, tax IDs, statements, and household plans remain in ignored paths or private systems.
