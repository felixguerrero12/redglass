# Smoke: fizz live strategies + exit protection (2026-08-11)

Date: 2026-08-11  
Host: `hermes chat -Q -s research/redglass --in /home/fg/fizz`  
Session: `20260811_023436_f7affb`  
Skill under test: redglass (intake + full graph + matrix completeness)  
Repo under analysis: `/home/fg/fizz` (live estate + exit docs)

## Question

Given today’s live strategy estate and risk/exit profiles, what is the most likely explanation for the main risk to exit/protection quality right now, and what must we watch next?

## Intake

```yaml
intake:
  is_analysis: true
  signals_fired:
    - competing stories (process outage vs single-seller design vs data drift)
    - high cost of error (exit/protection during active halt)
    - deception/concealment plausible (account scale unverified)
    - absence-as-proof risk (E4 “0% WR by design” must not clear halt/lease facts)
  mode: full_graph
  place: "incident / outage cause intersecting exit/protection quality"
```

## Facts used (collector)

| Id | Claim |
|---|---|
| E1 | 127 strategies; ~91 on `aggressive_morning`; almost all `lanes.live=false`; ~73 sim on that risk |
| E2 | `aggressive_morning` exits: hard_stop −25% (+ stop_flip), never_green, ratchet_stop, partial_profit, trail, max_hold; description says **gex_regime_shift removed** |
| E3 | `hand_trade_protect` separate: hard_stop −30%, never_green, partial_profit, trail +13/−3 |
| E4 | exit-attribution doc (2026-08-10): loss-exit 0% WR by design; shared risk; bad entries are the settled lever |
| E5 | `/api/ready=false`: HALT (95% DD), 25 unacked reconcile diffs, broker rate-limit; **lease:buy and lease:sell both held by ingest** |
| E6 | Protect/ExitRunner docs: exits need Book lots + sell-lease holder tick; stale process can serve old estate |
| E7 | `gex_dex_dip_q` → dedicated `gex_dex_dip_risk` (composition split exists) |

## Hypotheses

| Id | Statement (short) | Status |
|---|---|---|
| H1 | Main risk is halt/outage scale, not exit-rule mix (live lanes mostly off) | active |
| H2 | Structural single-seller under stress: ingest holds both leases; no Protect failover while halt+reconcile+RL stack | active |
| H3 | Data correctness: 25 discrepancies + RL → seller may act on wrong book | active |
| H4 | Deception/env confusion: halt dollars may be demo/paper scale | active (not rejected) |
| H5 | hand_trade_protect lots share single-lease exposure; distinct exit surface | active |

## Completeness

| Check | Result |
|---|---|
| Evidence × hyps | 7 × 5 = **35** cells |
| Missing pairs | `[]` |
| Reviewer item 9 | **PASS** |
| Reviewer overall | **pass** |

```text
RESMOKE_CHECK
MATRIX_COMPLETE: yes
CELL_COUNT: 35
MISSING_PAIRS: []
REVIEWER: pass
INTAKE_MODE: full_graph
```

## Ranking

| Hyp | Odds | Note |
|---|---|---|
| **H2** | **40–50%** | Lead. Single seller under stacked stress (not “lease bug”; Protect docs say monolith stays sole seller until promotion) |
| H3 | 25–35% | Concurrent driver with H2 (wrong book) |
| H5 | 15–25% | Parallel hand-lot surface; bite depends on open hand lots |
| H1 | 10–15% | Blast-radius modifier, not root mechanism |
| H4 | 5–10% | Kept alive pending account-scale check |

## Plain answer (from smoke)

Main risk today: one process (ingest) holds full exit authority while fighting halt, 25 unacked reconciliation discrepancies, and broker rate limiting. That matches documented sole-seller stage, not a surprise lease bug. The risk is **stacked stress on a single point of failure**.

Watch next:

1. Does halt block protective stop-exits, or only new entries?
2. Is `fizz-protect` deployed-idle or never started?
3. Is discrepancy count growing or flat?
4. Live vs demo scale behind $478.96 / $22.68
5. Open `hand_trade_protect` lot count

## Skill smoke verdict

| Gate | Result |
|---|---|
| Intake → full_graph | Pass |
| Full hop chain + investigation_log | Pass (10 hops) |
| Matrix completeness 35/35 | Pass |
| Deception hyp kept (H4) | Pass |
| Open-mind corrected mirror-imaging (lease-as-bug → designed single-seller) | Pass |
| Reviewer fail checklist | Pass |

**Skill smoke: PASS** for this scenario.

## Note on exit estate (today)

- Shared `aggressive_morning` still concentrates ~91 strategies (mostly sim).
- Dedicated risks exist (`whale_*`, `gex_dex_dip_risk`, `hand_trade_protect`, `stop_flip_risk`).
- Current `aggressive_morning.json` description: **gex_regime_shift removed** (differs from older attribution tables that still discuss it historically).

## Raw session

Local capture: `/tmp/hermes-smoke-fizz-exits.txt`  
Session id: `20260811_023436_f7affb`
