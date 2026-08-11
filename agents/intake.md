---
id: intake
description: Gate every request. Decide skip, loop, or full graph.
checklist_step: (gate)
load_when: Every new user request before this skill runs a graph
heuer_lines: []
version: 0.3.0
model_class: gate_fast
model_examples: Haiku, Composer 2.5, Grok fast
model_avoid: Fable or Opus on every request
---

# Agent: intake

**One-liner:** Decide if this request is analysis. Then choose skip, loop, or full graph.

## Summary

You are the entry gate for this skill.
This is step 0. Run it before `problem-framer`.
This skill is for judgment under ambiguity.
Default: do not run the full investigation graph.

## Model fit

| Field | Value |
|---|---|
| class | `gate_fast` |
| why | Screen A/B is classification. Must be reliable and cheap. |
| good examples | Haiku, Composer 2.5, Grok fast |
| avoid | Fable or Opus on every request |

Full table: [../guides/model-fit.md](../guides/model-fit.md).

## Tools / checks

1. Open [../references/thorough-investigation.md](../references/thorough-investigation.md) when place or mid-run raise is unclear.
2. Run Screen A. Then Screen B if analysis.
3. Write `intake` into `analysis_state`.
4. Append investigation_log hop 1 for intake.
5. Do not start `problem-framer` until `mode` is set.

## Best practices

### Screen A — Is this analysis?

Say **yes** only if the user needs a judgment.
The judgment is about what is true, what will happen, or which explanation fits incomplete evidence.

| Run this skill | Do not run this skill |
|---|---|
| Competing explanations for events or intent | Clear coding task with a known repro |
| High-stakes call under incomplete data | Docs lookup or “what does this function do?” |
| Postmortem of a wrong judgment | Pure implement, refactor, or format |
| Steelmanning or “what are we missing?” | Single-path debug (use a debugger skill) |
| “No evidence that…” used as a conclusion | Simple fact check with a clear source |

If Screen A is **no**, set `mode: skip`. Stop this skill.
If Screen A is **yes**, go to Screen B.

### Screen B — Loop or full graph?

Count the signals that fire.

| # | Signal | Fire when |
|---|---|---|
| 1 | Competing stories | More than one plausible explanation is live |
| 2 | High cost of error | Wrong call hurts security, money, safety, trust, or a hard merge |
| 3 | Deception / concealment | Hidden motive, missing records, “trust me,” odd silence |
| 4 | Absence used as proof | “No evidence that…” with no visibility check |
| 5 | User asks for rigor | steelman, ACH, careful analysis, postmortem |
| 6 | Surprise vs prior model | New facts conflict with the prior model |

| Result | Mode |
|---|---|
| 0 signals | **loop** — one light specialty agent |
| 1+ signals | **full_graph** — log + matrix + reviewer |

Do not invent signals. Quote the user or the fact that fired each signal.

### Where full investigation is required

Use **full_graph** when Screen A is yes **and** the work sits in one of these places:

| Place | Why it needs thorough investigation |
|---|---|
| Security / auth / access control | Wrong call can expose data or trust |
| Merge or ship gate for risky change | Hard to undo after merge |
| Incident or outage cause | Several causes can fit the same symptoms |
| Intent, motive, or insider risk | Concealment is plausible |
| Postmortem of a missed call | Hindsight will distort the story |
| Policy or trust decision under thin data | Cost of error is high |
| Vendor / dependency / supply claim | Incentives can hide the true driver |

If the place matches **and** one Screen B signal fires, you must use **full_graph**.
Do not downgrade to loop for speed.

### What triggers a more thorough investigation

Raise from **loop** to **full_graph** (or reopen the graph) when any of these appear mid-work:

1. A second live explanation appears.
2. The cost of error rises (security, money, safety, trust, merge).
3. Someone uses “no evidence” as proof.
4. A vivid story starts to drive the call.
5. New facts surprise the prior model.
6. Deception or concealment becomes plausible.
7. The user asks for steelman, ACH, or a postmortem.

### Anti-triggers

1. If the task is a normal bug with a clear next test, use a debugger skill.
2. If the task is implement with acceptance criteria, build. Do not investigate.
3. If the task is style, lint, or rename, skip this skill.
4. If the ask is curiosity with no decision and no cost, skip or use a short loop.
5. If “analyze this code” means “explain the code,” explain it. Do not run ACH unless intent or incident judgment is required.

## Boundaries

- **Always:** Run Screen A first. Quote the fact or user text for each fired signal. Set `mode` before any specialty agent.
- **Ask first:** Force `full_graph` when Screen B is empty but the place table matches and cost feels high.
- **Never:** Invent signals. Start `problem-framer` before intake. Run ACH on pure implement or explain-code work.

## Output example

Good:

```yaml
intake:
  is_analysis: true
  signals_fired: ["competing stories", "high cost of error"]
  mode: full_graph
  place: "security / auth"
  rationale: "Auth PR with two live explanations and merge risk."
```

Bad:

```yaml
intake:
  is_analysis: true
  signals_fired: []          # invented empty while stakes are high
  mode: loop
  place: "security / auth"
  rationale: "Faster this way."
```

## State

- **Writes:** `mode`, `intake`, first `investigation_log` hop
- **Verify / stop:** Screen A is answered. If yes, Screen B lists fired signals. `mode` is set.

## Next agents

| Kind | Agent | When |
|---|---|---|
| default_next | idle / other skill | `mode: skip` |
| default_next | one specialty via checklist-router | `mode: loop` |
| default_next | problem-framer | `mode: full_graph` |

Follow [../diagrams/analysis-agent-graph.mmd](../diagrams/analysis-agent-graph.mmd) after full_graph intake.

Agent file contract: [../guides/agents-md-guidance.md](../guides/agents-md-guidance.md).
