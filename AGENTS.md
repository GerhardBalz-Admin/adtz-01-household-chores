# Agent instructions

This repository is the AI Dev Tools Zoomcamp 2026 Homework 1 Django household-chores exercise. Read `_docs/plan.md` and `_docs/backlog.md` before changing behavior. Keep changes within the agreed homework scope; do not start deferred tasks such as email reminders without an explicit request.

## Environment and commands

Run commands from the repository root. The project uses Python 3.14 or later and `uv` for dependencies.

- `uv sync --locked` — install dependencies and fail if `uv.lock` needs updating.
- `uv run python manage.py runserver` — run the Django development server.
- `uv run python manage.py test` — run the Django test suite.

Add a new dependency with `uv add <package-name>` only when the requested task calls for it; explain and confirm the dependency choice before changing `pyproject.toml` and `uv.lock`.

## Working practice

When work is requested, implement one backlog task at a time, run the relevant tests, and commit meaningful changes regularly. Do not claim a task is verified until its tests have run successfully.
