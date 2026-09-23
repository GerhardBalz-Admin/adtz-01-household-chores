# Homework 1 answers

Answers to the [2026 Homework 1 questions](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/01-ai-native-workflow/homework.md). This file records the answers; it is not a course submission.

## Question 1: Coding agent

Claude Code.

## Question 2: Scope from the spec

The [project plan](plan.md) groups the intended scope into four features:

1. Email/password accounts and households that users can create or join.
2. Custom chores with a fixed rotation among household members.
3. Completion tracking with a timestamped history.
4. Due dates and overdue chores, with planned email reminders.

These are scope decisions; planned reminders should not be read as an implementation claim.

## Question 3: Django project

`settings.py` — in this repository, [`config/settings.py`](../config/settings.py) registers the apps.

## Question 4: First backlog task

**Accounts & households** — see [task 1 in the backlog](backlog.md#1-accounts--households).

## Question 5: Run the server

```sh
uv run python manage.py runserver
```

## Question 6: Run the tests

```sh
uv run python manage.py test
```

The earlier Homework 1 run reported 32 passing tests. The commands above are the standard explicit Python form of the course answers; this documentation change did not rerun the app or tests.
