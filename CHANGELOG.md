# Changelog

All notable changes to Foreman are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); this project uses semantic versioning.

## [Unreleased]

## [0.2.0] — 2026-08-12
### Added
- **Routing catalog** (`skills/orchestrator/references/routing.md`): task-shape →
  coworker+altitude table, a method for routing to whatever skills/agents are installed,
  parallelization rules, anti-patterns, and a fast decision procedure. Referenced from
  the orchestrator's Match step.
- **Token accounting** (`skills/orchestrator/references/token-accounting.md`): the
  **Plan line** convention — the manager states the cheapest routing it chose and why
  before dispatching, making the budget visible. Wired into the Budget step.
- **Worked examples** (`examples/`): three annotated end-to-end walkthroughs —
  parallel research, build-then-review with dependency waves, and knowing when *not*
  to orchestrate.
- **CI** (`.github/workflows/validate.yml`): runs `validate.py` and smoke-tests the
  SessionStart hook on every push and PR.
### Changed
- README: CI/version/license badges, a "What a run looks like" section, updated file
  tree and crew docs.

## [0.1.0] — 2026-08-10
### Added
- Initial plugin: `plugin.json` manifest and `marketplace.json` for installation.
- Core `orchestrator` skill — the 7-step manager protocol (intake → decompose → match
  → budget → dispatch → consolidate → record) with token-discipline rules.
- Specialized crew agents: `researcher`, `builder`, `reviewer`, plus a generic `worker`.
- `/manage <prompt>` command to run a request through the manager.
- SessionStart hook (`hooks/hooks.json` + `scripts/session-start.sh`) that surfaces the
  recent Run Log and reminds Claude of the manager role.
- `scripts/validate.py` — validates manifests and skill/agent/command frontmatter.
- Project memory (`CLAUDE.md`) with a Run Log and memory contract.
- MIT License, README, ROADMAP, `.gitignore`.
