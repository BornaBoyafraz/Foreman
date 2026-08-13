# Foreman

[![validate](https://github.com/BornaBoyafraz/Foreman/actions/workflows/validate.yml/badge.svg)](https://github.com/BornaBoyafraz/Foreman/actions/workflows/validate.yml)
&nbsp;![version](https://img.shields.io/badge/version-0.2.0-blue)
&nbsp;![license](https://img.shields.io/badge/license-MIT-green)

> Make Claude a manager: Foreman routes your prompt to the best skills and agents, runs them in parallel like coworkers, keeps token spend low, and keeps a running log of what it did.

**Foreman** is a Claude Code plugin. You give Claude a prompt; Foreman reads the goal,
breaks it into subtasks, picks the **cheapest capable** coworker for each (do it inline,
load a skill, or spawn an agent), runs the independent pieces **in parallel**, and shows
you its plan before spending anything.

Claude is the foreman. Skills and agents are the crew. Three to five of them can be
working at once.

## Contents
- [How to install](#how-to-install)
- [Quick start](#quick-start)
- [How it works](#how-it-works)
- [The crew](#the-crew)
- [What a run looks like](#what-a-run-looks-like)
- [Reading the Plan line](#reading-the-plan-line)
- [Memory: the Run Log](#memory-the-run-log)
- [Troubleshooting](#troubleshooting)
- [Update / uninstall](#update--uninstall)
- [Develop](#develop)
- [Project layout](#project-layout)
- [License](#license)

---

## How to install

Run these inside Claude Code:

```bash
# 1. Register this repo as a plugin marketplace
/plugin marketplace add BornaBoyafraz/Foreman

# 2. Install the plugin
/plugin install foreman
```

Working from a local clone instead? Point the marketplace at the folder:

```bash
/plugin marketplace add /path/to/Foreman
/plugin install foreman
```

Then reload/restart Claude Code so the skill, agents, command, and hook load.

**Confirm it's active.** Start a session in any project — Foreman's SessionStart hook
prints a short banner (and your recent Run Log, if any):

```
Foreman active — Claude is the manager, skills and agents are the crew.
- Route each subtask to the cheapest capable coworker: inline -> skill -> agent.
- Run independent subtasks in parallel (batch agent calls into one message).
- After each meaningful action, append a dated line to the "## Run Log" in CLAUDE.md.
```

No banner? See [Troubleshooting](#troubleshooting).

## Quick start

There are two ways to put Foreman to work:

**A. Explicitly, with the command:**

```
/manage add a /health endpoint, wire up logging, and write a test for each
```

**B. Just ask in plain language.** The manager triggers on its own when a request is
multi-part or parallelizable, or when you say words like *manage*, *orchestrate*,
*coordinate*, *delegate*, or *run these in parallel*:

```
Coordinate this: refactor the auth module, update the docs, and add tests — in parallel where you can.
```

For a small, single task you don't need Foreman at all — and it will say so rather than
over-managing (see [example 03](examples/03-know-when-not-to-orchestrate.md)).

## How it works

Foreman is really one idea: **Claude stops doing every task itself and starts managing.**
It breaks the work down, assigns each piece to whoever is best and cheapest, runs the
independent pieces at once, and stitches the results back together.

Under the hood it follows a **7-step protocol** (defined in
[`skills/orchestrator/SKILL.md`](skills/orchestrator/SKILL.md)):

1. **Intake** — restate the goal, catch blocking ambiguity.
2. **Decompose** — split into subtasks; mark each independent or dependent.
3. **Match** — assign each subtask to the cheapest capable coworker (see the ladder
   below). Uses the [routing catalog](skills/orchestrator/references/routing.md) when the
   choice isn't obvious.
4. **Budget** — batch parallel agents into one message; never spawn an agent just to read
   a file. Emit a [Plan line](#reading-the-plan-line) so the cost is visible first.
5. **Dispatch** — run independent waves concurrently; wait on dependencies.
6. **Consolidate** — merge the coworkers' outputs into one manager-level answer.
7. **Record** — append a dated line to the [Run Log](#memory-the-run-log).

### The cheapness ladder

Every subtask is assigned to the lowest rung that can still do the job:

> **inline  <  skill  <  agent**

| Rung | Cost | Use when |
|---|---|---|
| **inline** | ~free | trivial, single-file, or gluing coworker outputs together |
| **skill** | cheap (in-context) | an installed skill's trigger matches the subtask |
| **agent** | real (spawns context) | isolation, parallelism, a specialized type, or long multi-step work |

That's how token spend stays low: the manager keeps small work inline, prefers a skill
over an agent, and only spawns agents when there's a real reason. Full method:
[`token-accounting.md`](skills/orchestrator/references/token-accounting.md).

## The crew

The manager dispatches these coworkers (you don't call them directly — it picks them):

| Coworker | Role | Edits files? |
|---|---|---|
| `researcher` | Investigate: "where is X", "how does Y work", options for Z | No |
| `builder` | Implement one contained build subtask end to end | Yes |
| `reviewer` | Review a diff/files, return ranked findings | No |
| `worker` | Generic fallback when a subtask isn't cleanly research/build/review | Yes |

It will also use any **other** skills or agents installed in your environment when they
fit better — a UI skill, a docs skill, a domain-specific agent, the built-in `Explore`
and `Plan` agents, and so on.

## What a run looks like

Before doing any real work, the manager shows the routing it picked and why — the
**Plan line**:

```
Prompt: "Explain how auth, billing, and the job queue each work."

Plan (3 subtasks):
- #1 how auth works      → researcher (agent) — broad read-only search, don't self-read
- #2 how billing works   → researcher (agent) — independent of #1/#3
- #3 how the queue works → researcher (agent) — independent of #1/#2
Budget: 1 wave, 3 parallel researchers, 0 files read by the manager. Synthesis inline.

→ dispatches all 3 researchers in one message, waits, merges the briefs, and appends a
  line to the Run Log.
```

Full annotated walkthroughs live in [`examples/`](examples/) — including when the right
plan is **no coworkers at all**.

## Reading the Plan line

The Plan line is your chance to redirect Foreman *before* it spends anything:

- **Altitude** of each subtask: `inline` (Claude does it directly), `skill:<name>` (loads
  a skill), or `agent:<type>` (spawns a coworker).
- **Wave** = a batch of independent subtasks run at once. Dependent work waits its turn.

If the plan looks too heavy ("why is that an agent?"), just say so — e.g. *"do #1 inline
too"* — and it re-plans.

## Memory: the Run Log

After each meaningful action, Foreman appends a dated line to a `## Run Log` in your
project's `CLAUDE.md` (creating the file/section if missing):

```
- 2026-08-13 — Added /health + logging + tests. 2 parallel builders, review inline. Outcome: shipped, tests green.
```

Next session, the SessionStart hook surfaces the last few lines so Claude remembers what
already happened. You don't have to do anything — just let it keep the log.

## Troubleshooting

**No SessionStart banner / Run Log not surfacing**
- Confirm the plugin is installed and enabled, then restart Claude Code.
- The hook runs `scripts/session-start.sh`; ensure it's executable:
  `chmod +x scripts/session-start.sh`.

**The manager isn't triggering on plain-language requests**
- Use the explicit command: `/manage <your request>`. That always invokes the manager.

**"Is the plugin itself valid?"** (useful if you edit it)

```bash
python3 scripts/validate.py
```

Expected: `OK — 9 item(s) validated, no problems.`

## Update / uninstall

```bash
# update to the latest pushed version
/plugin marketplace update foreman-marketplace

# remove it
/plugin uninstall foreman
```

## Develop

Validate manifests and skill/agent/command frontmatter after any change:

```bash
python3 scripts/validate.py
```

CI runs the same check (plus a hook smoke-test) on every push and PR. See
[`ROADMAP.md`](ROADMAP.md) for what's next and [`CHANGELOG.md`](CHANGELOG.md) for history.

## Project layout

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
ROADMAP.md                        # what's next
CHANGELOG.md                      # release notes
LICENSE                           # MIT
```

## License

[MIT](LICENSE) © 2026 Borna Boyafraz
