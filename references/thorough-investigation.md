# Thorough investigation

This note states **when** to raise depth and **where** full investigation is required.
Use it with [../agents/intake.md](../agents/intake.md).

## Terms

| Term | Meaning |
|---|---|
| skip | Do not use this skill |
| loop | One specialty agent or a short checklist |
| full_graph | Full path with log, matrix, and skeptical-reviewer |

## Where full investigation is required

If the request is analysis (Screen A = yes) and it sits in one of these places, prefer **full_graph** as soon as one Screen B signal fires:

| Place | Required because |
|---|---|
| Security / auth / secrets / access | Wrong call can breach trust or data |
| Pre-merge / pre-ship risk gate | The change is hard to undo |
| Outage / incident cause | Many causes fit one symptom set |
| Motive / intent / insider risk | Concealment is a live option |
| Missed-call postmortem | Hindsight will rewrite memory |
| High-cost policy or trust call | Thin data, large downside |
| Vendor / dependency / supply claim | Incentives can distort the story |

If the place matches and the cost of error is high, do not stay in loop for speed.

## What triggers a more thorough investigation

### At intake (Screen B → full_graph)

1. Competing stories
2. High cost of error
3. Deception or concealment plausible
4. Absence used as proof
5. User asks for rigor
6. Surprise vs prior model

### Mid-run (raise loop → full_graph, or reopen graph)

1. A second explanation becomes live
2. Cost of error rises
3. “No evidence” appears as a conclusion
4. A vivid anecdote starts to drive the call
5. New facts conflict with the prior model
6. Deception becomes plausible
7. User asks for steelman, ACH, or postmortem
8. Matrix shows a zero-`I` tie between serious hyps
9. Reviewer fail checklist will fire (diagnostic gaps, holey matrix, mirror-imaging)

### After ship / after miss

1. Surprise vs milestones → return to evaluator or learner-postmortem
2. Confirmed miss → learner-postmortem, then intake again if a new judgment is needed

## What does not earn thorough investigation

1. Clear repro debug with a next experiment
2. Implement / refactor with acceptance criteria
3. Explain-code or docs lookup
4. Lint, format, rename
5. Low-cost curiosity with no decision

## Orchestrator rule

If intake set `mode: loop` and a mid-run trigger above fires:

1. Append an investigation_log note with the new trigger.
2. Set `mode: full_graph`.
3. Enter at the cheapest correct node (often `hypothesis-generator` or `evaluator`).
4. Do not finish with a loop ranking when a full_graph trigger is now true.
