# Operations

## Local run

```bash
PYTHONPATH=. python3 tests/check_portfolio_snapshot.py
```

## Docker run

```bash
mkdir -p data reports
LOCAL_UID=$(id -u) LOCAL_GID=$(id -g) docker compose build
LOCAL_UID=$(id -u) LOCAL_GID=$(id -g) docker compose run --rm fund-manager
```

The current container runs the verification check. It does not run a server or scheduler.

## Private data

Keep these outside Git and outside the image:

- `PLANNING.md`
- `data/`
- `reports/`
- `.env` and provider credentials
- downloaded statements and exported account data

The Compose bind mounts are explicit. Do not replace them with broad host mounts.

## Backup

Docker images and Git are not financial-data backups. Maintain encrypted, versioned backups of private records and document the backup date. Keep at least one copy off the primary computer. Back up source metadata and report provenance, not only derived totals.

## Recovery

1. Install Docker and Git on a replacement computer.
2. Clone the repository at the required commit.
3. Restore `PLANNING.md`, `data/`, `reports/`, and any secret-store entries from encrypted backup.
4. Create `data/` and `reports/` with appropriate ownership.
5. Build the image and run the container check.
6. Compare a restored report or checksum with the last verified backup.
7. Re-authenticate external integrations manually; never restore credentials into Git.

## Change control

Before a release or import change, inspect `git status`, the full diff, staged diff, and recent history. Run the native check, Docker check, compileall, and whitespace validation. Never claim a check passed unless it ran.

## Incident handling

If a source import is malformed, stale, duplicated, or ambiguous: stop the import, preserve the failure, record the source and error, and do not substitute zero. If credentials or account identifiers may have leaked, revoke or rotate them, remove the exposure from future reports, and record the incident privately.

## External systems

Drive and ERPNext are read-only during the current milestone. Any future write requires an explicit user request, narrow scope, dry-run or preview where possible, and a recorded result. Broker order submission remains out of scope.
