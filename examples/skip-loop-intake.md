# Example: skip and loop intake (not full graph)

Teaching example. Shows when intake stops this skill (**skip**) or runs one specialty (**loop**).
Compare with full-graph smokes: [service-outage-ach.md](service-outage-ach.md), [smoke-fizz-exits-ach.md](smoke-fizz-exits-ach.md).

Intake rules: [../agents/intake.md](../agents/intake.md).

---

## Case 1 — `skip` (not analysis)

### User ask

> Rename `getUser` to `fetchUser` in `auth.ts` and fix any broken imports. Keep behavior the same.

### Intake

**Screen A — Is this analysis?** No.  
This is implement/rename with clear acceptance criteria. No judgment under incomplete evidence.

```yaml
intake:
  is_analysis: false
  signals_fired: []
  mode: skip
  place: "n/a"
  rationale: >
    Pure rename/refactor. Anti-trigger: implement with acceptance criteria.
    Use a coding skill. Do not open ACH.
```

### What happens next

| Step | Action |
|---|---|
| This skill | Stop after intake. |
| Host | Run implement / refactor workflow. |
| Wrong path | Do **not** spawn `problem-framer` or build a matrix. |

### Investigation log (single hop)

```yaml
investigation_log:
  - hop: 1
    agent: intake
    heuer_lines: []
    reason: "Screen A no — not analysis."
    actions: ["Set mode skip", "Stop this skill"]
    state_writes: [intake, mode]
    verify_stop: passed
    routing_notes: {next_agent: idle, default_next: idle, consult: []}
```

---

## Case 2 — `loop` (analysis, zero Screen B signals)

### User ask

> One engineer said the deploy “felt wrong.” Logs look normal. No outage. No security stake.
> Quick read: is mirror-imaging the main risk in how we framed “felt wrong,” or is that overthinking?

### Intake

**Screen A — Is this analysis?** Yes.  
The ask is a judgment about framing / mind-set under thin anecdote data.

**Screen B — Signals**

| Signal | Fired? |
|---|---|
| Competing stories | No — one soft anecdote, not two live explanations |
| High cost of error | No — no outage, merge, or security gate |
| Deception / concealment | No |
| Absence used as proof | No |
| User asks for rigor | No — “quick read,” not ACH/steelmanning |
| Surprise vs prior model | No |

Zero signals → **loop**.

```yaml
intake:
  is_analysis: true
  signals_fired: []
  mode: loop
  place: "n/a"
  rationale: >
    Judgment about mind-set framing, but stakes are low and no competing
    incident story is live. One specialty pass is enough.
```

### What happens next

| Step | Action |
|---|---|
| Router | [../diagrams/checklist-router.mmd](../diagrams/checklist-router.mmd) → `open-mind` (mirror-imaging / stuck frame) |
| Do | Short open-mind pass: write assumptions, mirror-imaging check, stop |
| Do not | Full ACH matrix, skeptical-reviewer, or multi-hop graph |
| Raise later | If a second explanation or high cost appears mid-work, raise to `full_graph` (see [../references/thorough-investigation.md](../references/thorough-investigation.md)) |

### Loop result (sketch)

```yaml
mode: loop
assumptions:
  - "Felt wrong" is one vivid anecdote, not diagnostic evidence.
alternative_frame_notes:
  - Reframe: what would look the same if the deploy was fine and the engineer was tired?
routing_notes:
  next_agent: idle
  default_next: idle
```

No matrix. No odds table. That is correct for loop mode.

### Investigation log (two hops)

```yaml
investigation_log:
  - hop: 1
    agent: intake
    reason: "Screen A yes; Screen B zero signals → loop."
    state_writes: [intake, mode]
    verify_stop: passed
    routing_notes: {next_agent: open-mind, default_next: idle, consult: []}
  - hop: 2
    agent: open-mind
    heuer_lines: ["book/open-mind.md"]
    reason: "Mirror-imaging / frame check only."
    state_writes: [assumptions, alternative_frame_notes]
    verify_stop: passed
    routing_notes: {next_agent: idle, default_next: idle, consult: []}
```

---

## Case 3 — Same domain, but `full_graph` (contrast)

### User ask

> After the deploy, error rate jumped. Security team asks if it is a bad build, a platform change, or concealment in telemetry. We must decide before merge of the hot-fix.

### Why not loop

Screen A yes. Screen B fires: competing stories, high cost of error, deception plausible. Place matches outage + merge gate → **full_graph**.

Do not stay in loop for speed. See [service-outage-ach.md](service-outage-ach.md).

---

## Quick chooser

| Ask shape | Mode |
|---|---|
| Implement, rename, lint, explain-code, clear-repro debug | **skip** |
| Soft judgment, low cost, one specialty trigger | **loop** |
| Competing hyps, high cost, deception, or rigor ask | **full_graph** |

## Anti-patterns

1. Full graph on a rename because “maybe something is wrong.”  
2. Skip when the user asks for ACH / steelman / postmortem under incomplete evidence.  
3. Loop forever after a second live explanation appears — raise to full_graph.
