# Decisions

## 2026-10-05: Long-term manager, not trading bot

The product supports household planning and reports. Autonomous execution, liquidation-on-abstention, and conviction-based position sizing are excluded. Revisit only through a separately authorized scope change with risk controls.

## 2026-10-05: Python calculates; LLM explains

Financial arithmetic, validation, allocation, and scenario tables are deterministic Python. LLM output is optional, sourced, validated, and non-authoritative. An LLM failure leaves a missing memo, not a financial action.

## 2026-10-05: Standard library and SQLite first

Use native capabilities before dependencies. SQLite is the planned local store; it is not implemented yet. No speculative plugin system, multi-agent runtime, service mesh, or dashboard is required.

## 2026-10-05: Docker for redeployment

Docker provides a repeatable execution environment. Private data remains in explicit host directories and requires separate encrypted off-computer backups. The current image runs the portfolio check only.

## 2026-10-05: Source registry stays read-only

Drive statements and ERPNext records are evidence, not writable working copies. Preserve source IDs, dates, ownership, and correction history. Reconcile one complete period before broad import.

## 2026-10-05: Public repository, private household data

Architecture, source code, and synthetic checks are public. Household values, plans, account identifiers, tax details, statements, and secrets remain in ignored local paths or private systems.
