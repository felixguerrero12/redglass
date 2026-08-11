# ACH: Did we miss anything in the intake gate?

Dogfood on the intake design. Goal: use this skill for **analysis**, not everything.

## Problem

What most often makes hosts misuse this skill, and does `intake` block that?

## Hypotheses

| id | Statement |
|---|---|
| H1 | Trigger lists alone are enough; hosts will not run the skill on non-analysis work. |
| H2 | The main miss is a missing **“is this analysis?”** screen before signal counting. |
| H3 | The main miss is over-triggering on any uncertainty (including normal coding doubt). |
| H4 | Intake still fails without host Defaults that point at intake first. |

## Evidence

| id | Claim |
|---|---|
| E1 | Prior SKILL “When to use” listed analysis signals but no hard skip table for coding/explain/implement. |
| E2 | Smoke cases that earned full graph were judgment calls (auth intent), not “explain this function.” |
| E3 | Users asked for the skill not to run on everything. |
| E4 | Debugger skill already exists for clear repro bugs. |
| E5 | SOUL Defaults already load this skill for hard/ambiguous analysis — without an intake artifact, hosts may over-apply. |

## Matrix (short)

| | H1 | H2 | H3 | H4 |
|---|---|---|---|---|
| E1 | I | C | C | N |
| E2 | N | C | I | N |
| E3 | I | C | C | C |
| E4 | N | C | C | N |
| E5 | I | C | N | C |

## Ranking

| Hyp | Odds | Why |
|---|---|---|
| **H2** | **45–55%** | Fewest hard minuses; E1 shows the gap was the primary “is analysis?” gate. |
| **H4** | **20–30%** | Host wiring still matters after intake exists. |
| **H3** | **15–25%** | Real risk; anti-triggers in intake address it. |
| **H1** | **5–10%** | Inconsistent with E1 and E3. |

## Decision (patches)

1. Add `agents/intake.md` with Screen A (analysis?) then Screen B (loop vs graph).
2. Put anti-triggers for code/explain/implement.
3. Orchestrator step 0 = intake; diagram starts at intake.
4. Point SKILL teach-in and Hermes Defaults at intake.
5. Keep H4 open: verify Defaults mention intake.

## Skeptical-reviewer

Pass with residual risk: hosts can still ignore intake unless Defaults/SOP name it.
