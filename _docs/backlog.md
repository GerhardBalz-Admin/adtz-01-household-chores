# Backlog

## 1. Accounts & households
- Custom user model (email as username)
- Household model + membership (user ↔ household, many-to-many)
- Signup flow: create a household or join one via invite

## 2. Chores & rotation
- Chore model: name, household FK, frequency, rotation order (ordered list of members)
- Logic to compute "whose turn is it" and advance rotation on completion
- CRUD views/forms for households to create/edit/delete chores

## 3. Completion tracking
- ChoreCompletion model: chore FK, user FK, completed_at timestamp
- "Mark done" action that logs a completion and advances rotation
- History view listing past completions per chore/household

## 4. Due dates & overdue state
- Compute next due date per chore from frequency + last completion
- Dashboard view showing each chore's current assignee and due/overdue status

## 5. Email reminders
- Management command to send "chore due soon" and "chore overdue" emails
- Scheduling (cron / Celery beat / management command run periodically)

## 6. Polish
- Admin site registration for all models
- Basic tests for rotation and due-date logic
- Deployment config (env vars, static files, production settings)
