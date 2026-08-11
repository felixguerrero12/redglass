# Self-review ACH: is this skill highest quality? (refresh)

Dogfood run: this skill applied to itself.
Date: 2026-08-11 · Skill **redglass v0.0.1** · Mode: `full_graph`

Prior dogfood (same day, pre-intake/smoke era): conclusions archived at bottom.
This file is the **current** self-ACH.

## Problem (problem-framer)

**Question:** What most limits the chance that an agent using this skill will produce a high-quality judgment, and what must we change next?

**Assumptions:**
- Host agents follow written procedures imperfectly.
- Markdown + optional typed hops are the enforcement surface (no hard runtime).
- Effectiveness beats polish. Public push is optional.

## Hypotheses

| id | Statement | status |
|---|---|---|
| H1 | The skill is near ceiling for a markdown SOP; remaining gaps are polish (commit, naming, public push). | active |
| H2 | **Host compliance is still soft** — hosts can skip intake, matrix completeness, or investigation_log unless the operator insists. | active |
| H3 | The graph is **overbuilt**; too many nodes reduce compliance more than they add rigor. | active |
| H4 | Concealment / unknown: the main gap is **distribution and habit** — uncommitted pack + few operators means we still under-sample real misuse. | active |

## Evidence

| id | Claim | reliability | notes |
|---|---|---|---|
| E1 | Full stack present: intake gate, STE agents, model_fit, agents-md contract, install + AGENTS/CLAUDE, diagrams, required-inputs, matrix-completeness, investigation_log, effectiveness guide. | high | Design depth. |
| E2 | Prior entry bugs patched: collector lines include `1383–1387`; `references/required-inputs.md` exists; evaluator opens `ach-template.md`. | high | Closes old H2 drivers E2/E4/E5. |
| E3 | Live Hermes smokes recorded: auth-PR, auth-PR resmoke 48/48, fizz exits, skip/loop intake example. | high | Closes old “no live smoke” gap. |
| E4 | Matrix completeness once failed in smoke (E3 omitted) → reviewer gate patched; resmoke PASS. | high | Soft enforceability → written gate works when followed. |
| E5 | Typed hops: `hosts/compile_agent_hop.py --all` produces 12 hop pairs; `idle` sentinel; unittest PASS. Hops remain **optional**. | high | Helps Factor-2 hosts; non-users still soft. |
| E6 | Main path still runs bias-guard then open-mind on full_graph. | high | Cost; may be correct. |
| E7 | Multiple domains in examples now: service outage, auth PR, fizz exits, skip/loop, intake-gate ACH. | medium | Transfer risk lower than first dogfood. |
| E8 | Agent bodies STE + contract (Tools/checks, Boundaries, Output example); model_class on all 12 agents. | medium | Style/contract done; not diagnostic alone. |
| E9 | Large uncommitted pack on `main` (**redglass** v0.0.1 local vs last commit `f971e29` intake-era). No Phase C public push. | high | Distribution / habit risk. |
| E10 | No durable multi-host proof (Cursor/Claude/Codex) beyond install docs — Hermes is the proven host. | medium | Limits H1. |

## Matrix (diagnostic focus)

| Evidence | H1 | H2 | H3 | H4 | diagnostic? |
|---|---|---|---|---|---|
| E1 | C | N | N | N | weak (design ≠ compliance) |
| E2 | C | I | N | N | **yes** (old enforce gaps closed) |
| E3 | C | N | N | I | **yes** (smoke exists) |
| E4 | N | C | N | N | **yes** (hosts still cheat without gates) |
| E5 | C | C | N | N | weak (optional hops) |
| E6 | N | N | C | N | weak |
| E7 | C | N | I | N | weak |
| E8 | C | N | N | N | no |
| E9 | I | N | N | C | **yes** |
| E10 | I | C | N | C | **yes** |

## Ranking (work the minuses)

| hyp | odds | why |
|---|---|---|
| **H2** | **40–55%** | E4 shows compliance fails without gates; E5/E10 show most hosts still prose-only. Best remaining quality limiter. |
| **H4** | **25–35%** | E9 + E10: uncommitted + single proven host → we under-sample failure modes. |
| **H1** | **15–25%** | E2/E3/E7/E8 support near-ceiling *as designed*; E9/E10 keep it from winning. |
| **H3** | **5–15%** | Intake skip/loop already short-circuits; E7 argues breadth helps. No new smoke that shorter path beats full graph. |

## Rejected / deferred receipts

- Prior H2 (entry inconsistency) **largely closed** by E2; superseded by compliance-soft H2.
- Prior H4 (no live smoke) **rejected** as stated; replaced by distribution/habit H4.
- H3 not rejected; would rise if a live run skips bias/open-mind and quality holds.

## Skeptical-reviewer (on this ACH)

Fail checklist:

1. Single live hyp? **No** — four hyps kept.
2. Only `C` piles? **No** — ranking driven by `I` on H1 and prior-H4.
3. Deception/unknown dropped for no evidence? **No** — H4 kept on E9/E10.
4. Odds present? **Yes**.
5. Reject receipts? **Yes**.
6. Linchpins stated? **Yes** — imperfect host compliance; optional hops; Hermes-heavy evidence.
7. Mirror-imaging? **Watch** — do not assume every host is as careful as Hermes smoke sessions.
8. Vivid anecdote driving call? **No** — multiple smokes + repo facts.

**Verdict:** pass. Residual risk = **H2** (soft host compliance) + **H4** (thin distribution).

## Milestones (monitor)

- Commit redglass v0.0.1 pack → lower H4 slightly; does not fix H2.
- Second host smoke (Claude Code or Cursor) with intake skip + full_graph → lower E10 / H4.
- Host that uses generated hops and rejects illegal `next_agent` in the wild → lower H2.
- Live run that skips bias/open-mind with high-quality call → raise H3.

## Patch list (do now / soon)

1. **Commit** the uncommitted redglass v0.0.1 pack when the operator asks (closes part of H4).
2. Keep hops optional; document `--all` (done) — do not require hops for markdown hosts.
3. Prefer another host smoke over more agent files.
4. No graph shrink until a smoke supports H3.

## Lessons (learner-postmortem)

1. Dogfood ACH goes stale in hours when the skill moves fast — refresh after major packs.
2. Live smoke closes “unknown behavior” hyps; uncommitted work opens “unknown distribution” hyps.
3. Enforceability moved from missing docs → optional typed hops + operator discipline.

---

## Prior dogfood (archive)

First self-ACH on 2026-08-11 ranked **H2 entry/enforce gaps** (line-table mismatch, missing required-inputs, evaluator skipping ACH template, no smoke). Those patches landed; see E2–E4 above. Do not treat the archived ranking as current.
