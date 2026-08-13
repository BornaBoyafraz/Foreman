# Token Accounting

The manager spends tokens like they're its own. This doc defines the **Plan line** — a
compact, visible statement of the cheapest routing the manager chose, and *why* — so the
budget reasoning is explicit instead of hidden. Emit it at the end of **step 4 (Budget)**,
right before dispatching.

## Why make the budget visible
Routing is where tokens are won or lost. Writing the plan down does three things:
1. Forces the manager to actually pick the cheapest capable rung (inline < skill < agent).
2. Lets the user see and veto an over-eager fan-out before it costs anything.
3. Leaves a record the Run Log can reference.

## The Plan line

**Simple task (1–2 subtasks)** — one line is enough:

```
Plan: single-file edit → inline. No agents.
```

**Multi-part task** — a short block:

```
Plan (3 subtasks):
- #1 map the auth flow        → researcher (agent)   — broad read-only search, don't self-read
- #2 add the rate limiter     → builder (agent)      — contained, isolated from #3
- #3 add the audit log        → builder (agent)      — independent of #2 → run in same wave
Budget: 1 wave, 3 parallel agents, 0 redundant file reads. Consolidate + review inline.
```

## Rules the Plan line must obey
- **Name the altitude** for every subtask: `inline`, `skill:<name>`, or `agent:<type>`.
- **Justify each agent.** If a subtask says `agent`, one clause must say *why* it isn't
  cheaper (needs isolation / parallelism / a specialized type / long multi-step). No
  justification → it should have been `inline` or a `skill`.
- **State the waves.** How many sequential rounds, and how many agents run in parallel per
  round. Independent subtasks belong in the *same* wave (one message).
- **Call out what stays inline.** Consolidation, small edits, and glue work are almost
  always inline — say so, so it's clear you didn't spawn for them.

## Cheapness ladder (the whole game)

| Rung | Cost | Use when |
|---|---|---|
| **inline** | ~free | trivial, single-file, or gluing coworker outputs together |
| **skill** | cheap (in-context) | an installed skill's trigger matches the subtask |
| **agent** | real (spawns context) | isolation, parallelism, a specialized type, or long multi-step work |

If a subtask can be pulled down a rung without losing the outcome, pull it down. The
correct number of agents for a trivial subtask is **zero**.

## Anti-signals (your plan is probably too expensive if…)
- More than one agent shares most of the same context → collapse into one.
- An agent's whole job is to read a file or two → make it inline.
- Independent subtasks are split across multiple waves → merge into one parallel wave.
- You loaded a skill you never actually used → don't pre-load; load on match.
