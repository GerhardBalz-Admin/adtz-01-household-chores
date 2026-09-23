# Agent instructions

- Before changing application behavior, read `_docs/plan.md` and `_docs/backlog.md`.
- Use `uv` for Python dependency management.
- Work only on requested tasks; a backlog entry alone does not authorize implementation.
- Run relevant tests, report their results, and commit meaningful changes.

## Claude Code development record

- For Homework 1 development work, keep `_docs/claude-code-prompts.md` and `_docs/claude-code-conversation.md` aligned by session ID and coverage. The prompt log records the exact user prompts; the conversation file records the chronological, sanitized user and Claude dialogue and tool activity. Treat the original Claude Code session files as the evidence source. Never reconstruct missing content from a recap or repository history.
- At the beginning of each new development session, reconcile any earlier completed Homework 1 development session that is missing from either file. Before committing the current work, record the current session through the last completed turn available in the original transcript. If its final turn is not yet recorded, mark the session as partial in both files and finish it at the next development checkpoint. Do not claim that a session is complete until both files have been checked against its source.
- Apply the same session inclusion boundary in both files. Keep prompt-log maintenance sessions outside the development record unless they also perform Homework 1 development; identify any exclusion in the files' coverage notes. Label every public redaction or omission in the conversation file; inspect the staged diff for credentials and personal information before pushing. Keep original session files outside this public repository.
- Include documentation updates in the relevant development commit when the source transcript is available. If synchronization or safe publication is blocked, report the gap instead of inventing content or publishing an unsafe transcript.
