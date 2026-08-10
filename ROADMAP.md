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
- [ ] **Routing catalog** — a reference doc mapping common task shapes → the exact
      skill/agent to reach for, so matching is fast and consistent.
- [ ] **Token accounting** — a lightweight convention for the manager to note the
      cheapest plan it chose and why (visible reasoning, not guesswork).
- [ ] **Worked examples** — 2–3 end-to-end transcripts (`examples/`) showing a prompt
      decomposed, dispatched in parallel, and consolidated.
- [ ] **CI** — GitHub Action running `scripts/validate.py` on push/PR.
- [ ] Expand the crew only if a real gap shows up (e.g. `tester`, `docs`).

## Day 3 — Polish & release
- [ ] Dogfood Foreman on a real multi-part task and capture the transcript.
- [ ] Tighten skill wording based on how routing actually behaved.
- [ ] Screenshots / a short demo in the README.
- [ ] Tag `v0.2.0`, update `CHANGELOG.md`.

## Parking lot (maybe)
- A `Stop` hook that nudges when a session ended without a Run Log entry.
- A `/crew` command that lists available coworkers and when to use each.
- Per-project overrides for routing preferences.
