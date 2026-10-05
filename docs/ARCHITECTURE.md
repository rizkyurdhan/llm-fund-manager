# Architecture

## Status

This describes the target architecture and labels unfinished components explicitly. The current implementation only contains deterministic portfolio snapshot calculations and a Dockerized check.

## System boundary

```text
Private Drive / Sheets / ERPNext / later broker statements
                         |
                 read-only source adapters
                         |
                 validation and provenance
                         |
                  SQLite dated records
                         |
             deterministic Python calculations
                         |
             Markdown report and source table
                         |
       optional LLM research and explanation layer
                         |
                human review and decision journal
```

The application does not become the authority for bank, accounting, or broker balances. Source records remain read-only and preserve their file IDs, periods, and ownership.

## Components

- **Source registry:** records source location, file ID, statement period, extraction status, and checksum where available.
- **Import boundary:** validates trusted fields, normalizes dates/currencies, preserves source-row identity, and performs idempotent transactions.
- **SQLite ledger:** stores immutable source observations, corrections, classifications, policies, and report metadata. It is not yet implemented.
- **Calculation layer:** pure Python functions using `Decimal` or integer minor units. It must not call an LLM or broker.
- **Research layer:** optional one-LLM stage for source-backed explanations. It cannot change financial state or authorize actions.
- **Report layer:** renders calculation results, assumptions, gaps, sources, and memo status into Markdown.
- **Decision journal:** stores the human decision and authorization separately from analysis.
- **Docker runtime:** reproducible manual execution with a read-only root filesystem and host bind mounts for private data and reports.

## Trust boundaries

1. External files, web pages, spreadsheets, MCP responses, and LLM output are untrusted data.
2. Validation is required before external values enter calculations or storage.
3. Reports are outputs, not commands.
4. Broker, ERPNext, and Drive writes are disabled by default and require explicit authorization outside automated analysis.
5. Secrets are injected at runtime and never stored in images, Git, prompts, or reports.

## Data flow rules

- Preserve source and valuation time separately.
- Do not add Bank Transactions and GL Entries together.
- Do not count transfers between owned accounts as expenses or returns.
- Do not calculate performance from snapshots without cash-flow history.
- Do not merge holdings solely because their ticker matches.
- Keep current and post-sale scenarios separate until settlement is confirmed.

## Deployment shape

`Dockerfile` builds a small Python image. `compose.yaml` runs a manual service with dropped Linux capabilities, `no-new-privileges`, a read-only root, temporary filesystem, and explicit `data/` and `reports/` mounts. It is not yet a persistent web service, scheduler, or broker gateway.

## Deliberate ceilings

- One process, one LLM, manual runs, Markdown output, and native SQLite are intentional first-stage limits.
- Add a service API, scheduler, migrations, structured observability, or separate worker only when a concrete operational requirement and recovery test justify it.
