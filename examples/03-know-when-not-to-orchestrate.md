# Example 03 — Know when *not* to orchestrate

**Prompt:** *"There's a typo in the README — 'recieve' should be 'receive'. Fix it."*

The most important manager skill is recognizing when management is pure overhead. A good
manager does the one-line job itself.

---

### 1. Intake
Goal: fix one misspelling in `README.md`.

### 2. Decompose
One trivial, single-file edit. Nothing to split.

### 3. Match
Decision procedure, step 1: **"Trivial or single-file? → do it inline. Stop."**

### 4. Budget — Plan line
```
Plan: single-file typo fix → inline. No skills, no agents.
```

### 5. Dispatch
The manager edits `README.md` directly — `recieve` → `receive`.

### 6. Consolidate
Nothing to consolidate. Confirm the fix in one sentence.

### 7. Record
```
- 2026-08-12 — Fixed a typo in README (recieve→receive). Inline, no coworkers.
```

---

**Why this is the cheap plan:** spawning a `builder` to change one word would cost more
tokens and wall-clock than the edit itself, and produce a worse experience. The correct
number of coworkers here is **zero**.

> Anti-pattern this example guards against: "orchestration theater" — decomposing,
> dispatching, and consolidating work that a single inline edit finishes in one step.
