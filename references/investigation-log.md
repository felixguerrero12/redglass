# Investigation log

Append one entry to `analysis_state.investigation_log` after every agent hop.
This is the audit trail for the run. Ranking is the decision. The log is the process.

Write in simple technical English. See [../STYLE.md](../STYLE.md).

## Entry schema

```yaml
- hop: 1
  agent: problem-framer
  heuer_lines: ["book/problem-framer.md"]
  reason: "Wrong question / scope risk on merge decision."
  actions:
    - "Wrote problem statement."
    - "Listed starting assumptions."
  state_writes: [problem, assumptions]
  verify_stop: passed
  completeness: null          # or {ok: true, cells: 48, missing: []} after evaluator
  open_questions:
    - "Is a private security channel in use?"
  routing_notes:
    next_agent: hypothesis-generator
    heuer_lines: ["book/hypothesis-generator.md"]
    default_next: collector
    consult: []
```

## Field rules

| Field | Rule |
|---|---|
| `hop` | Integer. Start at 1. Increase by 1 each specialty hop (including consult). |
| `agent` | Id of the agent that just finished. |
| `heuer_lines` | `book/` section files handed to that agent. |
| `reason` | Why this agent ran (trigger or graph edge). One or two sentences. |
| `actions` | What the agent did. Bullet facts. No chat filler. |
| `state_writes` | Fields this hop changed. |
| `verify_stop` | `passed` or `failed` (plus short why if failed). |
| `completeness` | Required after `evaluator`. Else `null`. |
| `open_questions` | Gaps left for later hops. Can be `[]`. |
| `routing_notes` | Handoff used to leave this hop. |

## When to append

1. Finish the agent job.
2. Pass that agent verify/stop (or record `failed` and the re-entry).
3. Append the log entry.
4. Only then ask the orchestrator for the next handoff.

## Exception: intake

`intake` is hop 1 when the skill starts. It needs no prior log entry.
After intake finishes, every later hop must append a log entry before the next handoff.

## Good vs bad

Good: short facts, named state fields, explicit open questions.  
Bad: paste of the whole chat, missing `routing_notes`, hop skipped.

Worked fill: [../examples/investigation-log-auth-pr.md](../examples/investigation-log-auth-pr.md).
