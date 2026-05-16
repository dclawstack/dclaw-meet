---
date: 2026-05-16
tags: [decision, architecture]
---

# ADR-001: SQLite for Local Dev Environment

## Status
- [x] Accepted

## Context
The agent environment doesn't have Docker running. PostgreSQL can't be started locally. Tests and database initialization require a working relational database.

## Decision
Use `sqlite+aiosqlite` for local development and testing. Production continues to use PostgreSQL via the `DATABASE_URL` environment variable.

## Consequences
- **Easier:** No Docker dependency for local dev. Fast test execution.
- **Harder:** Alembic autogenerate generates empty migrations for SQLite (tables already managed by `init_db()`). Production migrations must be verified against PostgreSQL.
- **Mitigation:** CI pipeline runs against PostgreSQL. Manual migration review before production deploy.
