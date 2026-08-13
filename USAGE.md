# How to Use Foreman

A practical, step-by-step guide. For the big picture see the [README](README.md); for
the manager's internal protocol see [`skills/orchestrator/SKILL.md`](skills/orchestrator/SKILL.md).

---

## 1. Install

From GitHub (recommended):

```bash
/plugin marketplace add BornaBoyafraz/Foreman
/plugin install foreman
```

From a local clone instead:

```bash
/plugin marketplace add /path/to/Foreman
/plugin install foreman
```

Then reload/restart Claude Code so the plugin's skill, agents, command, and hook load.

## 2. Check it's working

Start a session in any project. Foreman's SessionStart hook prints a short banner and
your recent Run Log:

```
Foreman active — Claude is the manager, skills and agents are the crew.
- Route each subtask to the cheapest capable coworker: inline -> skill -> agent.
...
```

If you see that, you're set. (No banner? See [Troubleshooting](#7-troubleshooting).)

## 3. Run something

Two ways to put Foreman to work:

**A. Explicitly, with the command:**

```
/manage add a /health endpoint, wire up logging, and write a test for each
```

**B. Just ask in plain language.** The `orchestrator` skill triggers on its own when a
request is multi-part or parallelizable, or when you say words like *manage*,
*orchestrate*, *coordinate*, *delegate*, or *run these in parallel*:

```
Coordinate this: refactor the auth module, update the docs, and add tests — in parallel where you can.
```

For a small, single task you don't need Foreman at all — and it will tell you so rather
than over-managing (see [example 03](examples/03-know-when-not-to-orchestrate.md)).

## 4. Read the Plan line

Before doing any real work, the manager shows you the routing it picked and why — the
**Plan line**. This is your chance to redirect it *before* it spends anything:

```
Plan (3 subtasks):
- #1 refactor auth   → builder (agent)     — contained, isolated from #2/#3
- #2 update docs     → inline              — small, single file
- #3 add tests       → builder (agent)     — independent → same wave as #1
Budget: 1 wave, 2 parallel agents, docs inline. Review inline after.
```

- **Altitude** of each subtask: `inline` (Claude does it directly), `skill:<name>` (loads
  a skill), or `agent:<type>` (spawns a coworker).
- **Wave** = a batch of independent subtasks run at once. Dependent work waits for its
  wave.

If the plan looks too heavy ("why is that an agent?"), just say so — e.g. *"do #1 inline
too"* — and it will re-plan. Details: [token-accounting](skills/orchestrator/references/token-accounting.md).

## 5. Meet the crew

The manager dispatches these coworkers (see [the crew table](README.md#the-crew)):

| Coworker | Does | Edits files? |
|---|---|---|
| `researcher` | Finds things out ("where/how is X") | No |
| `builder` | Implements one contained subtask | Yes |
| `reviewer` | Reviews a diff, returns ranked findings | No |
| `worker` | Generic fallback | Yes |

You don't call these directly — the manager picks them. It will also use any *other*
skills/agents installed in your environment when they fit better (a UI skill, a docs
skill, a domain-specific agent, etc.).

## 6. The memory (Run Log)

After each meaningful action, Foreman appends a dated line to a `## Run Log` in your
project's `CLAUDE.md` (it creates the file/section if missing):

```
- 2026-08-13 — Added /health + logging + tests. 2 parallel builders, review inline. Outcome: shipped, tests green.
```

Next session, the hook surfaces the last few lines so Claude remembers what happened.
**You don't have to do anything** — just let it keep the log; skim it if you want the
history.

## 7. Troubleshooting

**No SessionStart banner / Run Log not surfacing**
- Confirm the plugin is installed and enabled, then restart Claude Code.
- The hook runs `scripts/session-start.sh`; check it's executable: `chmod +x scripts/session-start.sh`.

**The skill isn't triggering on plain-language requests**
- Use the explicit command: `/manage <your request>`. That always invokes the manager.

**"Is the plugin itself valid?"** (useful if you edit it)

```bash
python3 scripts/validate.py
```

Expected: `OK — 9 item(s) validated, no problems.`

## 8. Update / uninstall

```bash
# update to the latest pushed version
/plugin marketplace update foreman-marketplace

# remove it
/plugin uninstall foreman
```

---

**In one sentence:** install it, then either run `/manage <task>` or just ask Claude to
coordinate a multi-part job — it plans the cheapest routing, shows you the Plan line,
runs independent work in parallel, and logs what it did.
