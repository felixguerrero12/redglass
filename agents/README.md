# Analysis agents

Roster from the Heuer checklist router. Each file is one specialty node in the execution graph.

| id | Load when | Model class |
|---|---|---|
| [intake](intake.md) | **Step 0** — every request: analysis? loop or full graph? | `gate_fast` |
| [problem-framer](problem-framer.md) | Wrong question / scope fight | `intelligence_thinker` |
| [hypothesis-generator](hypothesis-generator.md) | Only one story feels obvious | `intelligence_thinker` |
| [collector](collector.md) | Tempted to pile confirming data | `agentic_worker` |
| [evaluator](evaluator.md) | Confirming favorite; ignore minuses | `intelligence_thinker` |
| [selector-reporter](selector-reporter.md) | Need odds + rejected hyps | `balanced_mid` |
| [monitor](monitor.md) | Surprise / change mind | `gate_fast` |
| [bias-guard](bias-guard.md) | Vivid anecdote, gaps, “no evidence” | `balanced_mid` |
| [open-mind](open-mind.md) | Mirror-imaging, stuck model | `intelligence_thinker` |
| [learner-postmortem](learner-postmortem.md) | Missed call, hindsight | `intelligence_thinker` |
| [orchestrator](orchestrator.md) | Routing after intake; caps; log gate | `gate_fast` |
| [skeptical-reviewer](skeptical-reviewer.md) | Review teeth after selector | `adversarial_reviewer` |

Each agent file has a **Model fit** section (class, examples, avoid) and follows the agent contract in [`../guides/agents-md-guidance.md`](../guides/agents-md-guidance.md) (Tools/checks, Boundaries, Output example).
Full model table: [`../guides/model-fit.md`](../guides/model-fit.md).

Canonical diagrams: [`../diagrams/`](../diagrams/). Practice board: [`../research/agent-practice-board.md`](../research/agent-practice-board.md).
Intake dogfood: [`../examples/intake-gate-ach.md`](../examples/intake-gate-ach.md).
Skip / loop examples: [`../examples/skip-loop-intake.md`](../examples/skip-loop-intake.md).
Thorough investigation (where + mid-run raise): [`../references/thorough-investigation.md`](../references/thorough-investigation.md).
