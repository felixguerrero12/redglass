# Re-smoke: auth PR after matrix-completeness gates

Date: 2026-08-11  
Host: `hermes chat -Q -s research/redglass`  
Session: `20260811_015038_ab4b3f`  
Commit under test: `3a20951` (matrix completeness four-gate fix)

## Same scenario

Quiet engineer → auth rewrite PR → no ticket → “trust me” → CVE blog on old lib → prior advocacy for old lib.

## Completeness result

| Check | Result |
|---|---|
| Evaluator completeness | **PASS** — 8×6 = **48** cells |
| Selector pre-rank check | **PASS** — 48/48 |
| Reviewer item 9 | **PASS** — missing pairs `[]` |
| E3 in YAML matrix | **Present** (6 cells: H1–H6) |

```text
RESMOKE_CHECK
MATRIX_COMPLETE: yes
CELL_COUNT: 48
MISSING_PAIRS: []
REVIEWER: pass
E3-omission class: FIXED
```

## Ranking (summary)

| Hyp | Odds | Note |
|---|---|---|
| H2 cover-up | 30–35% | Lead; zero `I`; motive from prior advocacy |
| H3 backdoor (deception) | 20–25% | Kept live; not disproved |
| H4 undisclosed mandate | 15–20% | Zero `I`; unverified private channel |
| H6 vendor collusion | 10–15% | Deception kept |
| H1 genuine fix | 5–10% | **Rejected** — three `I` marks |
| H5 burnout | 5–10% | Weak |

Residual risk (stated on pass): H2 vs H3 tied on hard minuses — evidence gap, not confirmation.

## Compared to first smoke

| Issue | First smoke | Re-smoke |
|---|---|---|
| Holey YAML matrix | Fail (E3 missing) | Fixed (48/48) |
| Completeness check named | No | Yes (evaluator + reviewer) |
| Reviewer item 9 | Would have been fail | Pass with empty missing list |

## Verdict

Matrix-completeness gates worked on this host run. Re-smoke **passes** the bug class that broke the first smoke.
