---
description: Run a prompt through the manager — Claude routes it to the best skills and agents, runs independent work in parallel, budgets tokens, and logs what it did to CLAUDE.md.
argument-hint: <what you want done>
---

Invoke the **orchestrator** skill and act as the manager for this request:

$ARGUMENTS

Follow the orchestrator protocol end to end:
1. Restate the goal.
2. Decompose into subtasks (mark independent vs. dependent).
3. Match each subtask to the cheapest capable coworker (inline → skill → agent).
4. Budget tokens — batch independent agents into one message; don't spawn to read.
5. Dispatch, waiting for dependent waves.
6. Consolidate into one manager-level answer.
7. Append a dated entry to the `## Run Log` in `CLAUDE.md`.

If the request is trivial, say so and just do it inline — don't over-orchestrate.
