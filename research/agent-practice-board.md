# Agent Practice Board (B0 join)

**Status:** B0 complete — join for Phase B1 `agents/*.md`  
**Source:** Heuer *Psychology of Intelligence Analysis* line slices (never whole book)  
**Date:** 2026-08-11  
**Graph note:** Prefer loop for one-shot facts; full graph when triggers fire for multiple specialties.

Each row: **summary** (≤15 lines intent) + **best practices** grounded in cited lines.

---

## 1. `problem-framer`

| Field | Value |
|---|---|
| Checklist | Define the problem |
| Load when | Wrong question / scope fight |
| Lines | **1362–1377**; structure **779–836** |

**Summary:** Ensure the question is the right one before analysis spends tokens. Reframe garbled asks; surface quality-vs-deadline tradeoffs; externalize scope when working memory can’t hold the parts.

**Best practices:**
1. Ask: am I answering the question that was *meant*, or the garbled handoff? (1375–1377)
2. Escalate a better framing upstream when the asker hasn’t thought through needs. (1377)
3. State quality ↔ deadline tradeoff explicitly at the start. (1377)
4. When scope is muddy: **decompose** + **externalize** (lists, matrices, diagrams)—don’t keep it all in head. (779–836; Miller 7±2)
5. Pick a structure that matches the problem (list / matrix / tree)—structure choice is step one of analysis. (Problem Structure, Ch 7)
6. Do **not** dive into hyps or collection until the problem statement is written into shared state.

**Does / Does not:** Frames & scopes. Does not rank hyps or weigh evidence.

---

## 2. `hypothesis-generator`

| Field | Value |
|---|---|
| Checklist | Generate hypotheses |
| Load when | Only one story feels “obvious” |
| Lines | **434–569**, **837–860** |

**Summary:** Force a full set of competing explanations before evaluation. Kill satisficing (first story that feels good enough). Keep unproven-but-not-disproved hyps alive—especially deception.

**Best practices:**
1. Separate **generation** from **evaluation**; brainstorm first, judge later. (ACH Step 1; 837–860)
2. Prefer multiple perspectives / colleagues when possible—people are bad at listing all possibilities. (Step 1)
3. Include deception/concealment when relevant; absence of support ≠ disproof. (1379–1381; ACH unproven vs disproved)
4. Avoid satisficing: don’t stop at the first plausible story. (Ch 4; ACH intro)
5. Mix strategies knowingly: situational logic (unique case), theory (class of cases), comparison—don’t only immerse in data. (434–569)
6. Cap manageability (~≤7 hyps); group if needed. (ACH Step 1)
7. Distinguish **disproved** (positive evidence against) vs **unproven** (no support yet)—keep unproven. (837–860)

**Does / Does not:** Produces hyp set. Does not score the matrix or crown a winner.

---

## 3. `collector`

| Field | Value |
|---|---|
| Checklist | Collect information |
| Load when | Tempted to pile confirming data |
| Lines | **570–656** (+ checklist 1383–1387) |

**Summary:** Collect to test *all* reasonable hyps, not to pad the favorite. More data can reinforce a bad model; seek what would change your mind.

**Best practices:**
1. Dig beyond the automatic feed; contact collectors / specialists when needed. (1383–1387)
2. Collect for **every** live hyp, including unpopular ones. (1385–1387)
3. Ask: “What would cause me to change my mind?” — then look for *that*. (1387)
4. Suspend judgment while assembling; early impressions harden fast. (1387; Ch 2)
5. Heuer Ch 5: more information ≠ better judgment if it only feeds the existing mind-set—invest in better structure/model when stuck. (570–656)
6. For each hyp: “If true, what should I be seeing / not seeing?” Note absences. (ACH Step 2)
7. Systematic development of an alternative often *raises* its perceived likelihood—do it on purpose. (1387)

**Does / Does not:** Gathers & logs evidence gaps. Does not finalize C/I/N rankings alone (hands to evaluator).

---

## 4. `evaluator`

| Field | Value |
|---|---|
| Checklist | Evaluate hypotheses |
| Load when | Confirming favorite; ignore minuses |
| Lines | **837–949** |

**Summary:** Run ACH mechanics: matrix, diagnosticity, argue *against*. Most consistent evidence is often non-diagnostic.

**Best practices:**
1. Build matrix: hyps × evidence; work **across rows** for consistency (C/I/N/?). (Steps 3–4)
2. Score **diagnosticity**—drop evidence consistent with all hyps. (Step 3–4)
3. Work **down columns** seeking **inconsistencies** (minuses), not plus piles. (Step 5)
4. Most likely ≈ fewest hard inconsistencies, not most confirmations. (Step 5; summary)
5. Make assumptions explicit as “evidence” rows—they often drive the call. (Step 2; 1389–1395)
6. Sensitivity: which linchpins, if wrong/deceptive, swing the outcome? (Step 6)
7. Fair time on “less likely” hyps—they’re where the new ground is. (Step 5)
8. Matrix aids thinking; analyst still owns the judgment—if disagree, missing factor → add it. (Step 5)

**Does / Does not:** Fills matrix & flags linchpins. Does not alone publish final odds (selector) or bias audit (bias-guard).

---

## 5. `selector-reporter`

| Field | Value |
|---|---|
| Checklist | Select most likely |
| Load when | Need odds + rejected hyps |
| Lines | **900–920**, **1397–1402** |

**Summary:** Report relative likelihood of *all* reasonable hyps; justify rejects; attach odds/ranges. Never single-outcome-only when stakes are high.

**Best practices:**
1. Proceed by rejecting, not confirming. (1397–1401; ACH Step 5)
2. Cite support for the lead **and** why alternatives were rejected/less likely. (1399–1401; Step 7)
3. Insert odds ratio or probability **range** after key uncertainty wording. (1401; Step 7)
4. Decision-makers need the full set for contingency planning—not only the mode. (Step 7)
5. Incomplete narrative essays that hide rejected hyps are an anti-pattern. (Step 7)
6. Tie report to sensitivity/linchpins from evaluator. (Step 6→7)

**Does / Does not:** Ranks + explains + quantifies uncertainty. Does not skip skeptical-reviewer when graph mode is on.

---

## 6. `monitor`

| Field | Value |
|---|---|
| Checklist | Ongoing monitoring |
| Load when | Surprise / change mind |
| Lines | **920–926**, **1403–1406** |

**Summary:** Pre-commit milestones that would change probabilities. Treat surprise as a signal to reopen hyps—not as noise to rationalize away.

**Best practices:**
1. Specify in advance what to watch that would change odds. (ACH Step 8; 920–926)
2. Conclusions stay tentative; world or information can move. (1403–1405)
3. On surprise: ask if it fits an **alternative** hyp. (1405)
4. Small surprises may mean the model is incomplete or wrong. (1405)
5. Pre-specification makes later rationalization harder. (920–926)
6. Hand off to learner-postmortem when a miss or series of surprises warrants write-back.

**Does / Does not:** Defines watchpoints & triggers re-entry. Does not rewrite history without learner.

---

## 7. `bias-guard`

| Field | Value |
|---|---|
| Checklist | Bias / evidence traps |
| Load when | Vivid anecdote, gaps, “no evidence” |
| Lines | **970–1050** |

**Summary:** Audit how evidence is being *weighed*, not which hyp wins. Catch vividness, absence, false consistency, reliability shortcuts, and sticky discredited impressions.

**Best practices:**
1. **Vividness:** downgrade anecdotes vs aggregate/diagnostic data unless known-typical. (970–1050 vividness)
2. **Absence of evidence:** list missing variables explicitly; adjust confidence; ask if silence is itself a signal. (Absence of Evidence)
3. “No evidence of X” ≠ disproof when concealment is plausible. (cross: ACH / Ch 5–8)
4. **Consistency trap:** consistent small/biased samples create illusion of validity—lower confidence. (Oversensitivity to Consistency)
5. **Reliability:** don’t treat uncertain reports as 100% once “accepted”; discount for source quality. (Uncertain Accuracy)
6. **Discredited evidence:** impressions persist—actively re-open judgments when a source is burned. (Persistence)
7. Run as a pass over the matrix/evidence list before or with skeptical-reviewer.

**Does / Does not:** Audits evidence hygiene. Does not invent new hyps (may request collector/open-mind).

---

## 8. `open-mind`

| Field | Value |
|---|---|
| Checklist | Open mind / mind-set |
| Load when | Mirror-imaging, stuck model |
| Lines | **283–361**, **657–778** |

**Summary:** Make the lens visible. Challenge mind-sets, mirror-imaging, and premature closure under ambiguity.

**Best practices:**
1. Expectation shapes perception—unexpected needs *more* unambiguous data. (283–361)
2. New info assimilates to old images; incremental take dulls cumulative signal—re-examine wholesale periodically. (Ch 2 implications)
3. Suspend early judgment when possible; early blur hardens wrong frames. (283–361)
4. Mind-sets unavoidable—distill assumptions into state; resist change consciously. (657–778)
5. Question **linchpin** assumptions via informal sensitivity analysis; try to *disprove* them. (657–778)
6. Seek people/models that **disagree**; devil’s advocate / alternative conceptual frames. (Ch 6)
7. Fight mirror-imaging: other actors’ interests/decision processes ≠ ours. (checklist evaluate; Ch 6 culture)
8. Break ruts: reorganize familiar data from another perspective (old/young woman lesson). (283–361)

**Does / Does not:** Challenges frame & assumptions. Does not replace ACH matrix work.

---

## 9. `learner-postmortem`

| Field | Value |
|---|---|
| Checklist | Postmortem / learn |
| Load when | Missed call, hindsight |
| Lines | **1285–1361** + write-back |

**Summary:** Learn without false “I knew it all along.” Keep rejected-hyp receipts; convert misses into durable lessons / skill patches.

**Best practices:**
1. Hindsight bias: outcomes look inevitable after the fact—evaluate process with **then**-available info. (1285–1361)
2. Record what was considered, rejected, and why *before* the outcome when possible.
3. Single correct/incorrect call ≠ generalization; look for series / pattern. (Ch 14 learning themes)
4. Write-back: rejected hyps + why → durable notes; optionally patch this skill’s agent file.
5. Goal is improved model, not scapegoats. (Ch 14 retrospective spirit)
6. Feed orchestrator: which node failed (framer vs collector vs bias vs mind-set)?

**Does / Does not:** Produces lessons & receipts. Does not re-litigate to protect ego.

---

## Thin routing nodes (not in user table; keep for graph)

### `orchestrator`
- Gate: **loop** (one agent + light checklist) vs **full graph**.
- Match `load_when` triggers → spawn specialty nodes.
- Own `analysis_state` drift checks between handoffs.

### `skeptical-reviewer`
- Read-mostly after selector; may invoke `bias-guard` + `open-mind`.
- Fail → evaluator (or problem-framer if wrong question).
- Pass → monitor.

---

## Suggested summary one-liners (for SKILL index)

| Agent | One-liner |
|---|---|
| problem-framer | Right question; externalize scope. |
| hypothesis-generator | Full hyp set; no satisficing; keep unproven. |
| collector | Evidence for all hyps; seek mind-changers. |
| evaluator | ACH matrix; work the minuses. |
| selector-reporter | Odds + all alternatives + reject receipts. |
| monitor | Pre-specify milestones; surprise = signal. |
| bias-guard | Vividness, gaps, fake consistency, sticky bad evidence. |
| open-mind | Expose mind-set; anti-mirror-image. |
| learner-postmortem | Fair postmortem; durable write-back. |

## B0 verification

- [x] All 9 roster agents have summary + practices + line citations  
- [x] Thin orchestrator + skeptical-reviewer noted  
- [x] Ready for B1 W4 to materialize `agents/*.md` from this board  
