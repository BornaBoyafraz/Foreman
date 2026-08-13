# Foreman — Project Memory

**Foreman** is a Claude Code **plugin** (repo: `claude-foreman`) that makes Claude act as
a **manager**. Claude reads a prompt, routes each piece of work to the best **skill** or
**agent** (its coworkers), runs independent pieces in parallel, keeps token spend low,
and records what it did here. Internal plugin name: `foreman`.

## What's in this plugin
- `.claude-plugin/plugin.json` — plugin manifest (name `foreman`, MIT, points hooks at `./hooks/hooks.json`).
- `.claude-plugin/marketplace.json` — makes it installable via `/plugin marketplace add` + `/plugin install`.
- `skills/orchestrator/SKILL.md` — **the core.** The manager protocol: intake → decompose → match → budget → dispatch → consolidate → record.
- `skills/orchestrator/references/routing.md` — task-shape→coworker catalog (loaded on demand from the Match step).
- `skills/orchestrator/references/token-accounting.md` — the **Plan line** + cheapness ladder (loaded from the Budget step).
- `agents/{researcher,builder,reviewer,worker}.md` — the crew the manager dispatches.
- `commands/manage.md` — `/manage <prompt>` runs a request through the manager.
- `hooks/hooks.json` + `scripts/session-start.sh` — SessionStart hook: surfaces the Run Log + manager reminder.
- `scripts/validate.py` — validates manifests + skill/agent/command frontmatter (`python3 scripts/validate.py`).
- `examples/` — three annotated end-to-end walkthroughs of the protocol.
- `.github/workflows/validate.yml` — CI: runs the validator + hook smoke-test on push/PR.
- `ROADMAP.md` / `CHANGELOG.md` / `README.md` / `LICENSE` — planning, history, docs, MIT.

## Memory contract (read this every session)
Claude keeps this file current. After each meaningful action:
1. Append a one/two-line dated entry to `## Run Log` below — goal, coworkers used, outcome.
2. If the plugin's structure or behavior changes, update the section above.
3. Keep it terse. This is a running log, not prose. Newest entries at the bottom.

## Run Log
- 2026-08-10 — Created the plugin from an empty directory: manifest, marketplace, orchestrator skill (manager protocol), worker agent, `/manage` command, README, and this memory file. Coworkers used: none (small scaffolding, done inline per the budget rule).
- 2026-08-10 — Named it **Foreman** (plugin name `foreman`); added MIT LICENSE and GitHub description; rewired plugin.json / marketplace.json / README / this file to the new name. Done inline.
- 2026-08-10 — GitHub repo is `github.com/BornaBoyafraz/Foreman` (corrects earlier `claude-foreman`). Improvement pass: added specialized crew (researcher/builder/reviewer), SessionStart hook + `session-start.sh`, `validate.py`, ROADMAP, CHANGELOG, `.gitignore`; updated orchestrator skill to route to the crew. Validator passes (9 items). Done inline. Initialized git and pushed to `main`.
- 2026-08-10 — Day 2 start: added routing catalog `skills/orchestrator/references/routing.md` (task-shape→coworker table, method for routing to installed skills/agents, parallelization rules, decision procedure) and wired it into the orchestrator Match step. Updated ROADMAP/CHANGELOG/README. Done inline. Validator passes (9 items; reference docs aren't frontmatter-validated).
- 2026-08-12 — Finished Day 2 + Day 3: token-accounting reference (the **Plan line** convention, wired into the Budget step), three annotated `examples/` walkthroughs, CI workflow (`validate.py` + hook smoke-test on push/PR), README demo section + badges. Bumped to **v0.2.0**, updated CHANGELOG/ROADMAP. Done inline (doc-writing — per the budget rule, no agents). Validator passes (9 items). Tagged `v0.2.0` and pushed.
