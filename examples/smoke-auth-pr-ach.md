# Smoke: auth PR full graph (live Hermes)

Date: 2026-08-11  
Host: `hermes chat -Q -s research/redglass`  
Session: `20260811_014500_8e3f1a`  
Commit under test: `91b62ab` (skill v0.6.0)

## Scenario

Senior engineer quiet for three days, then auth rewrite PR "for security," CI green, resists questions, no ticket, CVE blog on old library yesterday, prior advocacy for old library.

## Mode

`full_graph` — competing hyps, high stakes, deception risk.

## Result summary

| Check | Result |
|---|---|
| Full path order | Pass |
| routing_notes each hop | Pass |
| Deception hyps kept without support-only drop | Pass (H3, H5) |
| Ranking by minuses not C-count | Pass (H1 rejected on stacked `I`) |
| skeptical-reviewer run | Pass |
| Spend caps | Pass (10/16 steps) |
| Full book load | Pass (not loaded) |
| Matrix complete in final YAML | **Fail** — E3 present in prose table, missing from YAML `matrix:` list |

Lead ranking from the run: H6 embargo 30–40%, with do-not-merge until E5 timing + security-lead check.

## Hermes load note

`-s redglass` failed (`Unknown skill`).  
`-s research/redglass` worked.

## Skeptical-reviewer on the smoke (meta)

Fail checklist against the smoke artifact:

1. Multiple hyps? Pass.
2. Diagnostic `I` used? Pass.
3. Deception kept? Pass.
4. Odds present? Pass.
5. Reject receipts? Pass.
6. Linchpins stated? Pass.
7. Mirror-imaging checked? Pass.
8. Vivid quote not sole driver? Pass.
9. **NEW:** Every collected evidence id appears in `matrix` for active hyps? **Fail (E3 gap).**

## Patches from this smoke

1. Add matrix-completeness item to `skeptical-reviewer` fail checklist.
2. Document Hermes `-s research/redglass` in README adapters.
3. Add [../references/matrix-completeness.md](../references/matrix-completeness.md) with check algorithm.
4. Gate **evaluator** (must fill), **selector-reporter** (must not rank), **orchestrator** (must not spawn selector/reviewer on holey matrix), **skeptical-reviewer** (must fail and list missing pairs).

## Fix verification

Re-smoke the same prompt after these gates. Expect: either full E1–E8 cells in YAML, or an explicit reviewer/selector fail naming missing pairs — not a silent pass.

## H4 update (from skill self-review)

Live smoke exists now. H4 (repo-only blindness) drops. Residual risk: hosts can still omit matrix rows unless the reviewer fails them.
