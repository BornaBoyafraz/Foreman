# Foreman

[![validate](https://github.com/BornaBoyafraz/Foreman/actions/workflows/validate.yml/badge.svg)](https://github.com/BornaBoyafraz/Foreman/actions/workflows/validate.yml)
&nbsp;![version](https://img.shields.io/badge/version-0.2.0-blue)
&nbsp;![license](https://img.shields.io/badge/license-MIT-green)

> Make Claude a manager: Foreman routes your prompt to the best skills and agents, runs them in parallel like coworkers, keeps token spend low, and maintains a `CLAUDE.md` memory it updates as it works.

A Claude Code plugin. You give Claude a prompt; **Foreman** reads the goal, picks the
best **skills** and **agents** for each piece of work (its coworkers), runs the
independent pieces **in parallel**, spends **tokens** carefully, and logs what it did.

Claude is the foreman. Skills and agents are the crew. Three to five of them can be
working at once.

## Install

```bash
# 1. Register this repo as a plugin marketplace
/plugin marketplace add BornaBoyafraz/Foreman

# 2. Install the plugin
/plugin install foreman
```

Working from a local clone instead? Point the marketplace at the folder:

```bash
/plugin marketplace add /Users/borna/Programming/Skill\ Manager
/plugin install foreman
```

## Use

Run any request through the manager:

```
/manage build a landing page, wire up the contact form, and write tests for it
```

Or just ask Claude to "manage", "orchestrate", or "coordinate" a task — the
`orchestrator` skill triggers on its own for multi-part or parallelizable work.

## What a run looks like

The manager makes its budget visible with a **Plan line** before doing any work:

```
Prompt: "Explain how auth, billing, and the job queue each work."

Plan (3 subtasks):
- #1 how auth works      → researcher (agent) — broad read-only search, don't self-read
- #2 how billing works   → researcher (agent) — independent of #1/#3
- #3 how the queue works → researcher (agent) — independent of #1/#2
Budget: 1 wave, 3 parallel researchers, 0 files read by the manager. Synthesis inline.

→ dispatches all 3 researchers in one message, waits, merges the briefs, and appends a
  line to the Run Log in CLAUDE.md.
```

Full annotated walkthroughs live in [`examples/`](examples/) — including when the right
plan is **no coworkers at all**.

## How it works

The foreman follows a 7-step protocol (see `skills/orchestrator/SKILL.md`):

1. **Intake** — restate the goal, catch blocking ambiguity.
2. **Decompose** — split into subtasks, mark independent vs. dependent.
3. **Match** — assign each to the cheapest capable coworker: inline → skill → agent.
4. **Budget** — batch parallel agents into one message; never spawn an agent just to read.
5. **Dispatch** — run independent waves concurrently; wait on dependencies.
6. **Consolidate** — merge into one manager-level answer.
7. **Record** — append a dated line to the Run Log in `CLAUDE.md`.

## Token discipline

Foreman prefers the cheapest coworker that can do the job:

| Situation | Assigned to |
|---|---|
| Small edit / quick answer | Claude, inline |
| Task matches a skill's trigger | That skill |
| Broad "where/how" search | One `Explore` agent |
| Several independent chunks | Parallel agents (one message) |
| Deep multi-step effort | One specialized agent |
| Trivial subtask | No coworker at all |

## Files

```
.claude-plugin/plugin.json        # manifest
.claude-plugin/marketplace.json   # marketplace entry
skills/orchestrator/SKILL.md      # the manager protocol (core)
skills/orchestrator/references/routing.md          # task-shape -> coworker catalog
skills/orchestrator/references/token-accounting.md # the Plan line + cheapness ladder
agents/researcher.md              # read-only investigation coworker
agents/builder.md                 # implements a contained build subtask
agents/reviewer.md                # read-only review coworker
agents/worker.md                  # generic fallback coworker
commands/manage.md                # /manage <prompt>
hooks/hooks.json                  # SessionStart hook wiring
scripts/session-start.sh          # surfaces the Run Log + manager reminder
scripts/validate.py               # validates manifests + frontmatter
examples/                         # annotated end-to-end walkthroughs
.github/workflows/validate.yml    # CI: runs validate.py on push/PR
CLAUDE.md                         # project memory + run log
ROADMAP.md                        # what's next
CHANGELOG.md                      # release notes
LICENSE                           # MIT
```

## The crew

| Coworker | Role | Edits files? |
|---|---|---|
| `researcher` | Investigate: "where is X", "how does Y work", options for Z | No |
| `builder` | Implement one contained build subtask end to end | Yes |
| `reviewer` | Review a diff/files, return ranked findings | No |
| `worker` | Generic fallback when a subtask isn't cleanly research/build/review | Yes |

The manager also uses the environment's built-in agents (`Explore`, `Plan`, and any
domain-specific ones) when they're a better fit.

## Develop

Validate the plugin after changes:

```bash
python3 scripts/validate.py
```

## License

[MIT](LICENSE) © 2026 Borna Boyafraz
