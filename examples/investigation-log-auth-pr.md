# Example: investigation_log (auth-PR resmoke)

Backfill from Hermes session `20260811_015038_ab4b3f`.  
Shows a complete hop log for hosts. Pair with [smoke-auth-pr-resmoke.md](smoke-auth-pr-resmoke.md).

```yaml
investigation_log:
  - hop: 1
    agent: problem-framer
    heuer_lines: ["1362-1377", "779-836"]
    reason: "High-stakes merge decision with unclear real question."
    actions:
      - "Split the ask into technical risk vs process/intent."
      - "Wrote assumptions about CI and ticket visibility."
    state_writes: [problem, assumptions]
    verify_stop: passed
    completeness: null
    open_questions:
      - "Is there a private security or compliance channel?"
    routing_notes:
      next_agent: hypothesis-generator
      heuer_lines: ["434-569", "837-860"]
      default_next: collector
      consult: [open-mind]

  - hop: 2
    agent: hypothesis-generator
    heuer_lines: ["434-569", "837-860"]
    reason: "Only one story (genuine fix) felt obvious at first glance."
    actions:
      - "Created H1-H6 including deception hyps H3 and H6."
      - "Kept all six active; no early drop for lack of support."
    state_writes: [hypotheses]
    verify_stop: passed
    completeness: null
    open_questions:
      - "Which hyp is hurt by process-behavior evidence?"
    routing_notes:
      next_agent: collector
      heuer_lines: ["570-656", "1383-1387"]
      default_next: evaluator
      consult: [bias-guard]

  - hop: 3
    agent: collector
    heuer_lines: ["570-656", "1383-1387"]
    reason: "Need evidence for all hyps, not only confirming the favorite."
    actions:
      - "Logged E1-E8 including gaps E3/E8 visibility caveats."
      - "Listed open_collection for code audit and private-channel check."
    state_writes: [evidence, open_collection]
    verify_stop: passed
    completeness: null
    open_questions:
      - "Code audit not done."
      - "Private mandate not confirmed."
    routing_notes:
      next_agent: evaluator
      heuer_lines: ["837-949"]
      default_next: bias-guard
      consult: [open-mind, collector]

  - hop: 4
    agent: evaluator
    heuer_lines: ["837-949"]
    reason: "Build ACH matrix; work minuses."
    actions:
      - "Filled 8x6 matrix (48 cells)."
      - "Flagged E2 as low-diagnostic."
      - "Named linchpin: CI green is not security-safe."
    state_writes: [matrix]
    verify_stop: passed
    completeness: {ok: true, cells: 48, missing: []}
    open_questions:
      - "H2 vs H3 both have zero I marks."
    routing_notes:
      next_agent: bias-guard
      heuer_lines: ["970-1050"]
      default_next: open-mind
      consult: [collector]

  - hop: 5
    agent: bias-guard
    heuer_lines: ["970-1050"]
    reason: "Vivid 'trust me' quote and absence-of-ticket risk."
    actions:
      - "Capped vivid quote weight."
      - "Marked E3 reliability medium pending visibility check."
      - "Noted zero-I tie is a gap, not a win."
    state_writes: [evidence]
    verify_stop: passed
    completeness: null
    open_questions: []
    routing_notes:
      next_agent: open-mind
      heuer_lines: ["283-361", "657-778"]
      default_next: selector-reporter
      consult: []

  - hop: 6
    agent: open-mind
    heuer_lines: ["283-361", "657-778"]
    reason: "Mirror-imaging risk on trust and on suspicion."
    actions:
      - "Named trust mind-set and suspicion mind-set."
      - "Noted process-behavior alone cannot separate H1-like urgency from H3."
    state_writes: [assumptions]
    verify_stop: passed
    completeness: null
    open_questions: []
    routing_notes:
      next_agent: selector-reporter
      heuer_lines: ["900-920", "1397-1402"]
      default_next: skeptical-reviewer
      consult: [bias-guard]

  - hop: 7
    agent: selector-reporter
    heuer_lines: ["900-920", "1397-1402"]
    reason: "Need odds, rejects, and a ranked set."
    actions:
      - "Re-checked completeness 48/48."
      - "Ranked H2 lead; rejected H1 with receipt."
      - "Kept deception hyps H3 and H6 active."
    state_writes: [ranking, rejected_receipts, milestones]
    verify_stop: passed
    completeness: {ok: true, cells: 48, missing: []}
    open_questions:
      - "Need code audit to separate H2 and H3."
    routing_notes:
      next_agent: skeptical-reviewer
      heuer_lines: ["837-949", "970-1050", "657-778"]
      default_next: monitor
      consult: []

  - hop: 8
    agent: skeptical-reviewer
    heuer_lines: ["837-949", "970-1050", "657-778"]
    reason: "Full-graph review teeth before treating ranking as final."
    actions:
      - "Ran fail checklist items 1-9."
      - "Item 9 completeness PASS; missing []."
      - "Stated residual risk: H2/H3 zero-I tie."
    state_writes: [reviewer_verdict, lessons]
    verify_stop: passed
    completeness: {ok: true, cells: 48, missing: []}
    open_questions:
      - "Do not merge until audit or security-lead check."
    routing_notes:
      next_agent: monitor
      heuer_lines: ["920-926", "1403-1406"]
      default_next: idle
      consult: []

  - hop: 9
    agent: monitor
    heuer_lines: ["920-926", "1403-1406"]
    reason: "Pre-specify milestones after pass."
    actions:
      - "Wrote watch list for audit, mandate confirm, vendor tie, personal conflict."
      - "Set surprise protocol back to evaluator."
    state_writes: [milestones]
    verify_stop: passed
    completeness: null
    open_questions: []
    routing_notes:
      next_agent: idle
      heuer_lines: []
      default_next: idle
      consult: []
```
