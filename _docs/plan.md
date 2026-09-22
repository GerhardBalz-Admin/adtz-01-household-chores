# Plan: Household Chores Tool

## Scope

- **Multi-tenant Django web app** — users sign up, create/join a household
- **Individual accounts** (email/password), invited to a household
- **Custom chores** — households define chore name, frequency, and rotation order
- **Fixed rotation** assignment (auto-advances through members)
- **Completion tracking**: checkbox + timestamped history log
- **Reminders**: email nudges before/after due date
- **Missed chores**: stay visible as overdue (no auto-reassign, no verification)

## Stack

- Django
