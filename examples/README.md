# Examples

End-to-end walkthroughs of the manager protocol — each shows a prompt going through
intake → decompose → match → **Plan line** → dispatch → consolidate → Run Log.

They're written as annotated transcripts so you can see *why* the manager routed each
subtask the way it did, not just the final answer.

| # | Scenario | Teaches |
|---|---|---|
| [01](01-parallel-research.md) | "Explain how three subsystems work" | Fan-out to parallel `researcher`s in one wave |
| [02](02-build-and-review.md) | "Add two endpoints and check them" | Parallel `builder`s → `reviewer`, dependency waves |
| [03](03-know-when-not-to-orchestrate.md) | "Fix this typo" | The cheapest plan is often **no coworkers at all** |

The point of all three: the manager reaches for the **cheapest capable rung** (inline <
skill < agent), makes the budget visible with a Plan line, and only parallelizes work
that's genuinely independent.
