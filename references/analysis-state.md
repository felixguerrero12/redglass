# Shared analysis state

All specialty agents read and write this object.
One shared state turns separate agents into one system.

Use clear full sentences in string fields.

## Schema

```yaml
analysis_state:
  graph_version: "1"
  mode: skip | loop | full_graph
  intake:
    is_analysis: true | false
    signals_fired: [string]
    mode: skip | loop | full_graph
    place: string              # where in the work this sits, or "n/a"
    rationale: string
  problem: string
  assumptions: [string]
  hypotheses:
    - id: H1
      statement: string
      status: active | rejected | deferred
  evidence:
    - id: E1
      claim: string
      reliability: high | medium | low | unknown
      notes: string
  matrix:
    - evidence_id: E1
      hyp_id: H1
      mark: C | I | N | "?"
  ranking:
    - hyp_id: H1
      odds_or_range: string
      why: string
  rejected_receipts:
    - hyp_id: H3
      why: string
  milestones: [string]
  open_collection: [string]
  reviewer_verdict:
    pass: true | false
    issues: [string]
  lessons: [string]
  investigation_log:
    - hop: 1
      agent: string
      heuer_lines: [string]
      reason: string
      actions: [string]
      state_writes: [string]
      verify_stop: passed | failed
      completeness: null | {ok: bool, cells: number, missing: [string]}
      open_questions: [string]
      routing_notes:
        next_agent: string
        heuer_lines: [string]
        default_next: string | idle
        consult: [string]
  counters:
    reviewer_fail_cycles: 0
    consult_passes: 0
    heuer_slice_reads: 0
    total_agent_steps: 0
  routing_notes: |
    next_agent: string
    heuer_lines: [string]
    default_next: string | idle
    consult: [string]
    instruction: string
```

## Mark legend

| Mark | Meaning |
|---|---|
| `C` | Consistent with the hypothesis |
| `I` | Inconsistent with the hypothesis |
| `N` | Neutral / not useful |
| `?` | Unknown |

## Routing kinds

| Kind | Meaning |
|---|---|
| `next_agent` | Agent that runs now |
| `default_next` | Agent that runs after verify passes (from `analysis-agent-graph.mmd`) |
| `consult` | Optional short helper agent. Then return to the path |
| re-entry | Labeled edge on the diagram (fail, surprise, wrong question, miss) |

## Spend caps (orchestrator enforces)

| Counter | Default max |
|---|---:|
| `reviewer_fail_cycles` | 2 |
| `consult_passes` (per main-path node) | 3 |
| `heuer_slice_reads` (per agent turn) | 2 |
| `total_agent_steps` | 16 |

## Write rules

1. Each agent writes only the fields listed in its agent file.
2. Do not delete rejected hypotheses. Move them to `rejected_receipts`.
3. Keep `matrix` rows that still have diagnostic value.
4. If `reviewer_verdict.pass` is false, do not treat `ranking` as final.
5. After a miss, append to `lessons`.
6. Orchestrator must fill `next_agent`, `heuer_lines`, and `default_next` on every handoff.
7. Increment counters on each step, consult, slice read, and reviewer fail.
8. After each specialty hop, append one `investigation_log` entry before the next handoff. See [investigation-log.md](investigation-log.md).

## Diagrams (direction source)

- Entry by trigger: [../diagrams/checklist-router.mmd](../diagrams/checklist-router.mmd)
- Default next + re-entry: [../diagrams/analysis-agent-graph.mmd](../diagrams/analysis-agent-graph.mmd)
- Evidence picture: [../diagrams/ach-evidence-matrix.mmd](../diagrams/ach-evidence-matrix.mmd)

If an agent file and `analysis-agent-graph.mmd` disagree on `default_next`, trust the `.mmd`.

Worked example: [../examples/service-outage-ach.md](../examples/service-outage-ach.md).
Investigation log example: [../examples/investigation-log-auth-pr.md](../examples/investigation-log-auth-pr.md).
Effectiveness: [../guides/effectiveness.md](../guides/effectiveness.md).
