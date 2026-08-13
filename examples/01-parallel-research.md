# Example 01 — Parallel research

**Prompt:** *"I'm new to this repo. Explain how auth, billing, and the job queue each
work."*

This is three independent questions. The wrong move is to read a dozen files yourself
(floods context) or ask them one at a time (serial, slow). The manager fans them out.

---

### 1. Intake
Goal: give the user a clear picture of three subsystems — auth, billing, job queue.

### 2. Decompose
- **#1** How does auth work? — **[independent]**
- **#2** How does billing work? — **[independent]**
- **#3** How does the job queue work? — **[independent]**

None depends on another → they can all run at once.

### 3. Match
Each is a "find/understand across the codebase" shape → **researcher** (read-only, returns
a findings brief). Three independent questions → three researchers in one wave.

### 4. Budget — Plan line
```
Plan (3 subtasks):
- #1 how auth works       → researcher (agent) — broad read-only search, don't self-read
- #2 how billing works    → researcher (agent) — independent of #1/#3
- #3 how the queue works  → researcher (agent) — independent of #1/#2
Budget: 1 wave, 3 parallel researchers, 0 files read by the manager. Synthesis inline.
```

### 5. Dispatch
All three `researcher` agents are spawned **in a single message** so they run
concurrently. The manager waits for all three briefs to return.

### 6. Consolidate
The manager stitches the three briefs into one explanation, with `path:line` pointers,
and flags anything a researcher marked uncertain. Raw briefs are not pasted at the user.

### 7. Record
```
- 2026-08-12 — Onboarding: explained auth/billing/queue. 3 parallel researchers, synthesized inline. Outcome: overview delivered with file refs.
```

---

**Why this is the cheap plan:** the manager read **zero** files itself; each researcher
read only its slice; and the three ran in one wave instead of three serial turns.
