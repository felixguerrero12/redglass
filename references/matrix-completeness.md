# Matrix completeness rule

This rule fixes the smoke failure where prose listed evidence but YAML `matrix` dropped a row.

## Rule

For every evidence id in `analysis_state.evidence`, and every hypothesis with status `active` or `rejected` that was scored, `analysis_state.matrix` must contain a cell:

```text
{evidence_id, hyp_id, mark}
```

`mark` must be one of: `C`, `I`, `N`, `?`.

Deferred hyps may be omitted from the matrix only if `routing_notes` says they were not scored.

## Check algorithm (run before leaving evaluator)

1. Build set `E` = all `evidence[].id`.
2. Build set `H` = all `hypotheses[].id` where status is `active` or `rejected`.
3. Build set `M` = all `(evidence_id, hyp_id)` pairs in `matrix`.
4. For each `e` in `E` and each `h` in `H`, if `(e, h)` is not in `M`, the matrix is **incomplete**.
5. If incomplete, list the missing pairs. Do not hand off to `default_next`.

## Who enforces

| Agent | Action on incomplete matrix |
|---|---|
| `evaluator` | Must not stop. Fill missing cells first. |
| `selector-reporter` | Must not rank. Return to `evaluator` (re-entry). |
| `skeptical-reviewer` | Must **fail** (checklist item 9). Re-enter `evaluator`. |
| `orchestrator` | Before spawning `selector-reporter`, confirm the check passes. |

## Example

Evidence: E1, E2, E3. Active hyps: H1, H2.

Incomplete if `matrix` has E1×H1, E1×H2, E2×H1, E2×H2 but **no** E3×H1 / E3×H2.

That was the live smoke miss.
