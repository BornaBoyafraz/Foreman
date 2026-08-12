# Routing Catalog

The manager consults this during **step 3 (Match)**. Find the row whose *task shape*
matches the subtask, then reach for the listed coworker at the listed altitude. The
**cheapest capable option wins** — always try to drop a rung on this ladder:

> **inline  <  skill  <  agent**
>
> Do it yourself if you can. If a skill covers it, load the skill. Spawn an agent only
> when you need isolation, parallelism, a specialized type, or a long multi-step effort.

Routing has two layers: **Part A** is fixed (Foreman's own crew + built-in agents) and
always applies. **Part B** is how you match against whatever skills/agents happen to be
installed in the current environment — that set differs per project, so it's a *method*,
not a hardcoded list.

---

## Part A — Route by task shape (fixed)

| Task shape | Signals in the prompt | Reach for | Altitude |
|---|---|---|---|
| Quick factual answer about the code | "what does X do", one function/file | **Read it yourself** | inline |
| Small edit, rename, typo, one-liner | trivial, bounded to a line or two | **Yourself** | inline |
| Find where/how something works | "where is", "how is X wired", unfamiliar area | **researcher** (or `Explore`) | agent |
| Compare options / gather external info | "what are the options", "best way to", needs web | **researcher** | agent |
| Implement a contained change | "add", "build", "implement", bounded scope | **inline if 1 file**, else **builder** | inline / agent |
| Several independent build chunks | multiple unrelated features or files | **parallel builder agents** (one message) | agent ×N |
| Verify / review work | "review", "is this right", after a build lands | **reviewer** | agent |
| Debug a failure | "why is X failing", a stack trace, a red test | **researcher → builder → reviewer** (chain) | agents |
| Plan before building | "how should we approach", large fuzzy feature | **`Plan` agent**, then decompose | agent |
| Design / UI work | "landing page", "component", "make it look good" | **an installed UI skill** (see Part B) | skill |
| Produce a document | a file format named (docx, pptx, xlsx, pdf) | **the matching installed skill** | skill |

**Reading the table:** the further down the ladder you can stay, the cheaper. A one-file
implement is `inline`, not a `builder`. A broad search is a `researcher`, never "read 20
files yourself." A trivial edit gets *no* coworker.

---

## Part B — Route to whatever's installed (method)

Installed skills and agents vary by project, so don't memorize a list — **match by
description at dispatch time**:

1. **Skills announce their own triggers.** Each skill's description says when to use it.
   Match the subtask's keywords/intent to a skill's description; if it fits, load that
   skill. Example: a subtask "build a pricing table that looks polished" matches a UI
   skill whose description mentions components/landing pages/design → load it instead of
   hand-writing CSS in a `builder`.
2. **Prefer the most specific agent type available.** If the environment offers a
   domain-specific agent that fits, use it over `general-purpose`. Fall back to
   `Explore` (read-only search), `Plan` (design), or `general-purpose` only when nothing
   specific fits.
3. **When several could fit, break ties by:** skill over agent (cheaper), and
   more-specific over more-general. One good match beats three overlapping ones.
4. **When nothing fits,** use Foreman's own crew (`researcher` / `builder` / `reviewer`)
   or handle it inline.

> Rule of thumb: if you find yourself about to do a big task by hand that some installed
> skill clearly describes, stop and load the skill. That's the whole point of the manager.

---

## Part C — Parallelization rules

- **Batch independent agents into ONE message** so they run concurrently. 3–5 at a time
  is the sweet spot.
- **Never parallelize dependent steps.** If B needs A's output, A returns first.
- **Don't fan out work that shares most of its context** — one agent with a fuller brief
  beats three that each re-derive the same background.
- **A wave = all the `[independent]` subtasks you can start right now.** Run the wave,
  wait for returns, then start the next wave with what's now unblocked.

---

## Part D — Anti-patterns (don't)

- Spawning an agent to read a single file. (Read it inline.)
- Reading 20 files yourself to answer "where is X." (That's one `researcher`.)
- Loading five skills "just in case." (Load one when its trigger actually matches.)
- Running independent agents one-per-message. (Batch them.)
- Fanning out three agents that all need the same setup. (Use one.)
- A `builder` for a one-line change. (Inline.)

---

## Decision procedure (fast path)

For each subtask, in order — take the first that applies:

1. **Trivial or single-file?** → do it **inline**. Stop.
2. **Does an installed skill's description match?** → **load that skill**. Stop.
3. **Is it "find/understand" across the codebase or web?** → **researcher** (parallel if
   several independent questions). Stop.
4. **Is it a contained build?** → **builder** (parallel builders if several independent
   chunks). Stop.
5. **Is it "check/verify" of existing work?** → **reviewer**. Stop.
6. **Is it big and fuzzy?** → **`Plan` agent** to design, then re-run this procedure on
   the resulting subtasks.
7. **Otherwise** → generic **worker**, tightly briefed.
