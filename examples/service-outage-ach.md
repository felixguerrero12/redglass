# Example: service outage ACH (full graph)

This is a **teaching example**. It shows a finished `analysis_state` and the handoff pattern.
It is not a claim about a real outage.

Scenario: After a deploy, error rate jumps. One story feels obvious ("bad deploy").

## Mode

`full_graph` — competing hyps, high user impact, confirming-data temptation.

## Final analysis_state (abridged)

```yaml
analysis_state:
  graph_version: "1"
  mode: full_graph
  problem: >
    What is the most likely cause of the error-rate jump after deploy 2026-08-11,
    and what must we watch next?
  assumptions:
    - Metrics pipeline latency is under 2 minutes.
    - The deploy touched the API service and a shared library.
  hypotheses:
    - id: H1
      statement: The new API build introduced a latent bug under production load.
      status: active
    - id: H2
      statement: A dependency or platform change coincided with the deploy window.
      status: active
    - id: H3
      statement: Traffic shape changed (bot spike / bad client) and only looks deploy-linked.
      status: active
    - id: H4
      statement: Concealment or incomplete telemetry hides the true fault domain.
      status: deferred
  evidence:
    - id: E1
      claim: Error spike began within 3 minutes of deploy finish.
      reliability: high
      notes: Time correlation only. Not diagnostic alone.
    - id: E2
      claim: Rollback of API build cut errors by ~80% within 5 minutes.
      reliability: high
      notes: Strong against pure traffic-shape story.
    - id: E3
      claim: Sibling services on the same cluster stayed flat.
      reliability: medium
      notes: Weakens broad platform story. Does not kill a shared-library fault.
    - id: E4
      claim: One engineer anecdote of "seen this on last release too."
      reliability: low
      notes: Vivid. Downweighted by bias-guard.
  matrix:
    - {evidence_id: E1, hyp_id: H1, mark: C}
    - {evidence_id: E1, hyp_id: H2, mark: C}
    - {evidence_id: E1, hyp_id: H3, mark: C}
    - {evidence_id: E2, hyp_id: H1, mark: C}
    - {evidence_id: E2, hyp_id: H2, mark: "?"}
    - {evidence_id: E2, hyp_id: H3, mark: I}
    - {evidence_id: E3, hyp_id: H1, mark: C}
    - {evidence_id: E3, hyp_id: H2, mark: I}
    - {evidence_id: E3, hyp_id: H3, mark: N}
    - {evidence_id: E4, hyp_id: H1, mark: N}
    - {evidence_id: E4, hyp_id: H2, mark: N}
    - {evidence_id: E4, hyp_id: H3, mark: N}
  ranking:
    - hyp_id: H1
      odds_or_range: "55-70%"
      why: Fewest hard inconsistencies; rollback response fits; E1 alone was non-diagnostic.
    - hyp_id: H2
      odds_or_range: "15-25%"
      why: Sibling flatness is a hard minus for broad platform; shared-library path still open.
    - hyp_id: H3
      odds_or_range: "10-20%"
      why: Rollback improvement is a hard minus for pure traffic-shape.
  rejected_receipts:
    - hyp_id: H3
      why: Not fully rejected. Parked as low. E2 is a hard minus for "traffic only."
  milestones:
    - Shared-library bisect shows the fault outside the API build → raise H2.
    - Error signature matches a known bot pattern with deploy held constant → raise H3.
    - Second rollback of only the library with API fixed fails to help → raise H1 further.
  open_collection:
    - Diff shared library vs API-only changes in the same release train.
  reviewer_verdict:
    pass: true
    issues: []
  lessons: []
  counters:
    reviewer_fail_cycles: 0
    consult_passes: 1
    heuer_slice_reads: 2
    total_agent_steps: 11
  routing_notes: |
    next_agent: monitor
    heuer_lines: ["920-926", "1403-1406"]
    default_next: idle
    consult: []
```

## Handoff sketch (what good routing looks like)

```text
orchestrator → problem-framer → hypothesis-generator → collector
  → evaluator → bias-guard (consult skipped second time; E4 already downweighted)
  → open-mind → selector-reporter → skeptical-reviewer (pass) → monitor
```

Example mid-graph `routing_notes`:

```yaml
next_agent: evaluator
heuer_lines: ["837-949"]
default_next: bias-guard
consult: [open-mind]
instruction: >
  Open agents/evaluator.md.
  Work minuses. E1 is likely non-diagnostic.
  If stuck, read only 837-949.
```

## Why this example is effective

1. H1 was not crowned because of time correlation alone (`E1` consistent with all).
2. Hard `I` marks moved the ranking.
3. Vivid anecdote did not drive the call.
4. Odds, rejects, and milestones are present.
5. Reviewer passed on diagnostic structure, not on confidence theater.

Copy this shape. Replace the domain content. Keep the discipline.
