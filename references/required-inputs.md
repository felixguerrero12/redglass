# Required inputs by agent

Orchestrator handoff verify uses this table.
If a required field is missing, do not spawn the agent.

| Agent | Required in `analysis_state` before start |
|---|---|
| `intake` | none (first agent); writes `intake` + `mode` |
| `problem-framer` | raw ask available (may be outside state); `intake.mode` is `loop` or `full_graph` |
| `hypothesis-generator` | `problem`, `assumptions` |
| `collector` | `hypotheses` with at least one `active` |
| `evaluator` | `hypotheses`, `evidence`, `assumptions` |
| `bias-guard` | `evidence` (and `matrix` if already started) |
| `open-mind` | `assumptions`, `problem` |
| `selector-reporter` | `matrix` that passes [matrix-completeness.md](matrix-completeness.md); `evidence`; `hypotheses` |
| `skeptical-reviewer` | `ranking`, `matrix`, `rejected_receipts`, `evidence` (to re-check completeness) |
| `monitor` | `ranking` |
| `learner-postmortem` | full state + outcome or surprise note |
| `orchestrator` | none beyond intent to route |

Also required on every handoff in `routing_notes`:

- `next_agent`
- `heuer_lines`
- `default_next`
- `consult` (list; can be empty)
