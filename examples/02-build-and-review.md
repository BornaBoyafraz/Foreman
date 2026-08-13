# Example 02 — Build in parallel, then review

**Prompt:** *"Add a `GET /health` endpoint and a `POST /feedback` endpoint, then make
sure they're solid."*

Two independent builds, followed by a check that depends on both. This shows **dependency
waves**: some work runs in parallel, some has to wait.

---

### 1. Intake
Goal: two new endpoints, implemented and verified.

### 2. Decompose
- **#1** Implement `GET /health` — **[independent]**
- **#2** Implement `POST /feedback` (validate body, persist) — **[independent]**
- **#3** Review both endpoints for correctness/edge cases — **[depends: #1, #2]**

### 3. Match
- #1 — small, but two independent endpoints touching separate files → a **builder** each,
  in parallel. (If #1 were literally a two-line handler in the same file as #2, the
  manager would fold it inline instead.)
- #2 — contained build with validation + persistence → **builder**.
- #3 — "check existing work" shape → **reviewer** (read-only, ranked findings).

### 4. Budget — Plan line
```
Plan (3 subtasks, 2 waves):
  Wave 1 (parallel):
  - #1 GET /health      → builder (agent)  — independent slice, own files
  - #2 POST /feedback   → builder (agent)  — independent slice, own files
  Wave 2 (after #1+#2):
  - #3 review both      → reviewer (agent) — needs the finished code to review
Budget: 2 waves, max 2 parallel agents. Manager wires routes + fixes nits inline.
```

### 5. Dispatch
- **Wave 1:** both `builder`s spawned in one message. Manager waits for both to report.
- **Wave 2:** once both builds land, spawn the `reviewer` with the diff.

### 6. Consolidate
Manager applies any trivial reviewer nits **inline** (not worth another builder), and
surfaces only real findings to the user with a ship / fix-first verdict.

### 7. Record
```
- 2026-08-12 — Added GET /health + POST /feedback. Wave 1: 2 parallel builders. Wave 2: reviewer. Applied 1 nit inline. Outcome: both endpoints shipped, reviewer verdict = ship.
```

---

**Why this is the cheap plan:** independent builds ran together (one wave, not two turns);
the reviewer was a single read-only pass instead of a second full build; and small fixes
were folded inline rather than spawning a third builder.
