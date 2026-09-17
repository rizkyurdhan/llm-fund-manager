# LLM Fund Manager

Personal, long-term investment planning and portfolio research. Standalone application using [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) as a source reference, accessed with [opensrc](https://github.com/vercel-labs/opensrc).

## Status

Documentation stage, 2026-09-17. No application, broker connection, or scheduled service implemented. No upstream application code copied. Household records belong in private Sheets, Obsidian, and ignored local files, not this public repository.

## Proposed architecture

```text
Google Sheets / later statement imports
                 |
          import and validate
                 |
         SQLite dated snapshots
                 |
       deterministic Python analysis
                 |
      LLM research and explanation <--- sourced product documents
                 |
        validate proposed actions
                 |
       Markdown report / Obsidian
                 |
          human decision journal
```

- **Input:** preserve owner, platform, product, valuation date, currency, value, and source. Preserve source-row identity; a shared ticker does not imply a duplicate holding.
- **Storage:** snapshot imports are transactional and idempotent. Corrections retain provenance. A repeated import must not add capital. Distinguish valuation time from import time.
- **Calculations:** use integer minor units or `Decimal` for money. Compute allocation, concentration, scenario losses, and retirement projections independently of the LLM. Quote-currency values do not establish economic currency exposure.
- **Policy:** human-approved allocation and constraints. A loss tolerance is not a guaranteed drawdown ceiling. Planned asset sales remain scenarios until actual settlement.
- **Research:** one LLM initially; source-backed explanations and structured proposals. External documents are evidence, never executable instructions. LLM output is untrusted input.
- **Output:** render financial tables directly from calculation results. Validate proposal amounts and limits in code. LLM failure leaves the numeric report available with an explicit missing-memo status; it never triggers liquidation.
- **History:** retain inputs, policy version, sources, model/prompt metadata, memo, and human decision. Do not treat deposits as investment gains; return calculations require cash-flow history.
- **Integration:** MCP can read Sheets and update Obsidian interactively. A scheduled application will need its own authenticated MCP client or Google API access, with credentials outside Git. Honcho supplies context, not authoritative balances.

Python + SQLite + Markdown is the proposed starting stack. Provider and data APIs remain unselected. IBKR is a potential reporting source first; order submission is a separate, future scope requiring explicit authorization.

## First milestone

1. Import a dated Sheets snapshot, preserving household ownership and product types.
2. Validate amounts, dates, missing fields, and duplicate-import behavior.
3. Produce allocation and explicit stress scenarios with source references.
4. Generate a sourced LLM memo without inventing missing facts.
5. Save a report and decision record; verify malformed input, unchanged reimports, and LLM failure paths.

Retirement projection follows once expense assumptions are available. Contribution recommendations require an approved target allocation and actual available cash. Scheduling follows a reliable manual run.

## Source reference

```bash
npx --yes opensrc fetch virattt/ai-hedge-fund
npx --yes opensrc path virattt/ai-hedge-fund
```

Inspected on 2026-09-17: upstream commit [`fc1bf250ead209ae5f02c39c3d0062c4bb554505`](https://github.com/virattt/ai-hedge-fund/tree/fc1bf250ead209ae5f02c39c3d0062c4bb554505), package version `2.2.0`.

`opensrc` is a development tool, not a runtime dependency. Its cache does not retain `.git`; nine reviewed files were verified using Git blob hashes against that commit's GitHub tree. Fetching `main` later may return different code: reverify before attributing changes to this revision.

| Reviewed upstream file | Applicable lesson / boundary |
| --- | --- |
| `hedge_fund/fund/spec.py` | Validated, serializable mandate; household policy does not need strategy pods. |
| `hedge_fund/pipeline/run_cycle.py` | Separate stages; upstream directly submits broker orders and can target a flat book on abstention. Do not copy that behavior into savings management. |
| `hedge_fund/pipeline/models.py` | Self-contained decision record with input policy and output details. |
| `hedge_fund/portfolio/construction.py` | Conviction normalization can allocate a full gross target to one weak signal. Do not use LLM confidence as household capital allocation. |
| `hedge_fund/risk/limits.py` | Deterministic position/gross limits and recorded clamp events; these are not drawdown guarantees. |
| `hedge_fund/risk/test_limits.py` | Check limit invariants and explainability; reference tests inspected, not executed. |
| `hedge_fund/signals/llm_agent.py` | Distinguish data failure from LLM abstention; cache and validate responses. |
| `pyproject.toml` | Upstream depends on Pydantic, LangChain providers, numerical libraries, and Textual. No dependency stack adopted. |
| `LICENSE` | MIT, copyright 2024 Virat Singh. Preserve notice if code is copied later. |

Reference review is focused, not a full audit. Current reuse is conceptual only. Household accounting, unit-linked insurance, mortgage scenarios, and retirement spending require purpose-built logic.

## Documentation

- [AGENTS.md](AGENTS.md): working rules for coding agents.
- `PLANNING.md`: private, ignored local household baseline. Not distributed with this repository.
- Obsidian: private project journal and source links; no automatic bidirectional synchronization promised.
