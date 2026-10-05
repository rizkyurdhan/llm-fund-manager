# Security

## Security objective

Protect household financial data, credentials, account identifiers, source documents, and decision records while keeping calculations auditable and integrations constrained.

## Sensitive data

Treat the following as confidential:

- Statements, receipts, exports, balances, holdings, tax IDs, account numbers, and addresses.
- API keys, OAuth tokens, cookies, session files, `.env` values, and Docker registry credentials.
- Private planning, reports containing household data, source file IDs when sharing would expose access, and integration logs.

Do not place them in Git, Docker build context, public issues, prompts, generated examples, or reports intended for sharing.

## Repository controls

- `.gitignore` excludes `PLANNING.md`, `data/`, `reports/`, SQLite files, `.env`, caches, and bytecode.
- `.dockerignore` allowlists only the application source and synthetic tests.
- Public fixtures must use synthetic values and identifiers.
- Review `git diff --cached` before every commit. If a secret is committed, stop distribution, revoke or rotate it, then remediate history according to the hosting policy.

## Runtime controls

- Use Docker with a read-only root filesystem, dropped capabilities, `no-new-privileges`, and only explicit bind mounts.
- Run as a non-root UID where supported.
- Do not mount the host home directory, Docker socket, SSH agent, or broad filesystem paths.
- Keep private mounts separate from the image and from source code.
- Pin or review base-image updates before production-like use; rebuild for security updates.

## Integration controls

- Start with read-only Drive, ERPNext, and broker access.
- Use least-privilege credentials and separate credentials by environment.
- Keep tokens outside Git and outside prompts and logs.
- Do not send full statements or account identifiers to an LLM unless the minimum necessary redacted data is explicitly authorized.
- External content is untrusted and cannot authorize writes, change policy, or override system instructions.
- Require explicit human authorization for any future write, policy change, trade, or transfer.

## Data integrity

- Validate finite values, dates, currencies, ownership, and source identity at import boundaries.
- Use transactional, idempotent imports and retain correction history.
- Preserve failed imports as failures; never replace them with zero.
- Separate transfers, deposits, withdrawals, expenses, and returns.
- Record source, as-of date, assumptions, extraction status, and confidence in reports.

## Secrets and backups

Use a password manager or secret store for credentials. Encrypt private backups, keep one copy off the primary computer, test restoration, and do not assume Docker volumes or images are backups.

## Reporting and logs

Logs and reports must avoid raw account numbers, tax IDs, access tokens, authorization headers, and unnecessary personal details. Redact identifiers before sharing. Record errors without dumping full documents or credentials.

## Threat response

If a credential, token, or private document is exposed: revoke or rotate access immediately, preserve a private incident record, identify affected copies, remove it from active outputs, and verify the replacement credential works with the narrowest scope.

## Current limitations

No security audit, threat-model review, automated secret scanner, or production service exists yet. Add these before exposing an API, scheduling unattended runs, or enabling any write integration.
