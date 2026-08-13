# Foreman — Roadmap

A short, living plan for the next few days. Check items off as we go; the source of
truth for *what actually happened* is the Run Log in `CLAUDE.md`.

## Day 1 — Foundation ✅
- [x] Plugin scaffold: `plugin.json`, `marketplace.json`.
- [x] Core `orchestrator` skill — the 7-step manager protocol + token budget.
- [x] `/manage` command.
- [x] Project memory (`CLAUDE.md`) with a Run Log + memory contract.
- [x] Specialized crew: `researcher`, `builder`, `reviewer` (+ generic `worker`).
- [x] SessionStart hook that surfaces the Run Log and the manager reminder.
- [x] `scripts/validate.py` — manifest + frontmatter checks.
- [x] MIT License, README, `.gitignore`.
- [x] Push to GitHub.

## Day 2 — Depth
- [x] **Routing catalog** — `skills/orchestrator/references/routing.md`: maps task
      shapes → the exact coworker + altitude, a method for matching installed
      skills/agents, parallelization rules, and a fast decision procedure. Wired into
      the orchestrator's Match step.
- [x] **Token accounting** — the **Plan line** convention
      (`references/token-accounting.md`): the manager states the cheapest routing it
      chose and why before dispatching. Wired into the Budget step.
- [x] **Worked examples** — three annotated transcripts in `examples/` (parallel
      research; build-then-review with dependency waves; when *not* to orchestrate).
- [x] **CI** — `.github/workflows/validate.yml` runs `validate.py` + hook smoke-test on
      push/PR.
- [ ] Expand the crew only if a real gap shows up (e.g. `tester`, `docs`). *(deferred —
      no gap yet.)*

## Day 3 — Polish & release ✅
- [x] Dogfood the manager pattern; the `examples/` walkthroughs came out of it.
- [x] Tighten skill wording: Match step points to the routing catalog; Budget step
      requires a Plan line.
- [x] Demo in the README ("What a run looks like" + badges). *(No screenshots — Foreman
      is a text/CLI plugin; an annotated transcript is the honest demo.)*
- [x] Tag `v0.2.0`, update `CHANGELOG.md`.

## Parking lot (maybe)
- A `Stop` hook that nudges when a session ended without a Run Log entry.
- A `/crew` command that lists available coworkers and when to use each.
- Per-project overrides for routing preferences.
