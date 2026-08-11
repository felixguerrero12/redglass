---
name: redglass
description: "Judge under ambiguity with checklist agents and ACH."
version: 0.0.1
author: fg (adapted from Richards J. Heuer, Jr.)
license: MIT
---

# Redglass

Judgment under ambiguity — Heuer checklist agents and ACH. Learn from misses.

This skill is for **any agent**. It is not tied to one runtime.
It is for **analysis**, not for every coding or lookup task.

Primary method: intake gate + Heuer checklist + specialty agents + shared state.
Write project prose in simple technical English. See [STYLE.md](STYLE.md).

## Teach-in

1. Install for your host: [guides/install.md](guides/install.md).
2. Read [agents/intake.md](agents/intake.md) — Screen A/B before any graph.
3. Read [guides/how-to-use.md](guides/how-to-use.md).
4. Read [guides/effectiveness.md](guides/effectiveness.md).
5. Skim [examples/service-outage-ach.md](examples/service-outage-ach.md) before your first full-graph run.
6. Skim [examples/skip-loop-intake.md](examples/skip-loop-intake.md) before your first skip or loop decision.
7. Maintainers: [examples/intake-gate-ach.md](examples/intake-gate-ach.md) and [examples/skill-self-review-ach.md](examples/skill-self-review-ach.md).

## Files

| File | Use |
|---|---|
| [agents/intake.md](agents/intake.md) | Step 0 — analysis? loop or full graph? |
| [guides/how-to-use.md](guides/how-to-use.md) | Step guide for agents |
| [guides/install.md](guides/install.md) | Install on Hermes, Cursor, Claude, chat hosts, or any agent |
| [guides/effectiveness.md](guides/effectiveness.md) | What raises call quality |
| [guides/model-fit.md](guides/model-fit.md) | Model class per agent (thinker / mid / agentic / gate) |
| [guides/agents-md-guidance.md](guides/agents-md-guidance.md) | How to write specialty agent files (GitHub lessons adapted) |
| [research/12-factor-agents-mapping.md](research/12-factor-agents-mapping.md) | 12-Factor Agents map + own-your-prompts style |
| [hosts/](hosts/) | Optional typed-hop compile from `agents/*.md` (Factor 2) |
| [examples/service-outage-ach.md](examples/service-outage-ach.md) | Worked full-graph example |
| [examples/skip-loop-intake.md](examples/skip-loop-intake.md) | Worked skip and loop intake (not full graph) |
| [examples/skill-self-review-ach.md](examples/skill-self-review-ach.md) | Dogfood ACH on this skill |
| [examples/intake-gate-ach.md](examples/intake-gate-ach.md) | Dogfood ACH on the intake gate |
| [agents/](agents/) | Specialty agents per checklist action |
| [diagrams/](diagrams/) | Mermaid graph sources (`.mmd`) |
| [references/source.md](references/source.md) | Heuer line ranges (slice only) |
| [references/ach-template.md](references/ach-template.md) | ACH matrix template |
| [references/analysis-state.md](references/analysis-state.md) | Shared state schema |
| [references/required-inputs.md](references/required-inputs.md) | Handoff input gate |
| [references/matrix-completeness.md](references/matrix-completeness.md) | Every evidence × hyp cell present |
| [references/investigation-log.md](references/investigation-log.md) | Per-hop process audit trail |
| [references/thorough-investigation.md](references/thorough-investigation.md) | Where full investigation is required; mid-run raise triggers |
| [examples/smoke-fizz-exits-ach.md](examples/smoke-fizz-exits-ach.md) | Live smoke: fizz strategies + exit protection |
| [examples/investigation-log-auth-pr.md](examples/investigation-log-auth-pr.md) | Backfilled log from auth-PR resmoke |
| Book path | `book/` section files via [references/source.md](references/source.md) (never load all of `book/`) |

## When to use

Run [agents/intake.md](agents/intake.md) first.

- Screen A must say this is **analysis** (judgment under incomplete evidence).
- Then Screen B chooses **loop** or **full_graph**.

Do **not** use this skill as the default for implement, explain-code, lint, or clear-repro debug work.

## Loop or full graph

Intake owns this decision. Summary:

| Signal count (Screen B) | Mode |
|---|---|
| Not analysis (Screen A no) | **skip** |
| Analysis, 0 signals | **loop** |
| Analysis, 1+ signals | **full_graph** |

**Where** full investigation is required (security, merge gate, outage, motive, postmortem, high-cost trust, vendor claim): see [references/thorough-investigation.md](references/thorough-investigation.md).
**When** to raise mid-run from loop to full_graph: same note.

## Checklist → agent

| Checklist step | Load when | Agent | Heuer section |
|---|---|---|---|
| Define the problem | Wrong question / scope fight | [problem-framer](agents/problem-framer.md) | [book/problem-framer.md](book/problem-framer.md) |
| Generate hypotheses | Only one story feels obvious | [hypothesis-generator](agents/hypothesis-generator.md) | [book/hypothesis-generator.md](book/hypothesis-generator.md) |
| Collect information | Tempted to pile confirming data | [collector](agents/collector.md) | [book/collector.md](book/collector.md) |
| Evaluate hypotheses | Confirming favorite; ignore minuses | [evaluator](agents/evaluator.md) | [book/evaluator.md](book/evaluator.md) |
| Select most likely | Need odds + rejected hyps | [selector-reporter](agents/selector-reporter.md) | [book/selector-reporter.md](book/selector-reporter.md) |
| Ongoing monitoring | Surprise / change mind | [monitor](agents/monitor.md) | [book/monitor.md](book/monitor.md) |
| Bias / evidence traps | Vivid anecdote, gaps, "no evidence" | [bias-guard](agents/bias-guard.md) | [book/bias-guard.md](book/bias-guard.md) |
| Open mind / mind-set | Mirror-imaging, stuck model | [open-mind](agents/open-mind.md) | [book/open-mind.md](book/open-mind.md) |
| Postmortem / learn | Missed call, hindsight | [learner-postmortem](agents/learner-postmortem.md) | [book/learner-postmortem.md](book/learner-postmortem.md) |

Routing helpers: [intake](agents/intake.md), [orchestrator](agents/orchestrator.md), [skeptical-reviewer](agents/skeptical-reviewer.md).

## Core rules

1. Mind-sets always exist. Write them down. Challenge them.
2. More data is not better judgment if it only feeds the old model.
3. Reject hypotheses. The lead story often has the least hard evidence against it.
4. "No evidence" is not proof of absence when concealment is plausible.
5. Bias awareness is not a cure. Use the procedures.
6. Surprise is a signal. Reopen the graph.

## Learn write-back

After a miss or a hard graph run:

1. Record rejected hypotheses and why.
2. Store one durable lesson for this domain.
3. Patch an agent file in this skill when the lesson is reusable.

## Anti-patterns

- Load the full Heuer file into context.
- Jump to a favorite story and skip agents.
- Confirm the favorite. Ignore minuses.
- Say "no evidence of X" with no visibility check.
- Skip `skeptical-reviewer` in full-graph mode.
- Ignore spend caps in `agents/orchestrator.md`.
- Choose `default_next` without reading `diagrams/analysis-agent-graph.mmd`.
- Skip `intake` and run full graph on implement/explain/debug work.
- Edit this skill without updating the dogfood ACH when entry tables change.
