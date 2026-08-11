# How to use this skill (for agents)

This guide is procedural. Follow the steps in order.

Write all new prose for this project in simple technical English.
See [../STYLE.md](../STYLE.md).

## Before you start

1. If this host is new to the skill, follow [install.md](install.md).
2. Read [../agents/intake.md](../agents/intake.md).
3. Read [../SKILL.md](../SKILL.md).
4. Read [effectiveness.md](effectiveness.md).
5. Optional host setup: pick model classes from [model-fit.md](model-fit.md).
6. When you edit an agent file, follow [agents-md-guidance.md](agents-md-guidance.md).
7. Open the shared state schema in [../references/analysis-state.md](../references/analysis-state.md).
8. Keep the Heuer book file outside the prompt. Use line ranges only.
9. Default book path: `~/psychology-of-intelligence.md`.
10. Skim [../examples/service-outage-ach.md](../examples/service-outage-ach.md) once if this is your first full-graph run.
11. Skim [../examples/skip-loop-intake.md](../examples/skip-loop-intake.md) once if this is your first skip or loop decision.

## Step 1 — Start state shell

1. Create an `analysis_state` object from the schema.
2. Set `graph_version` to `1`.
3. Set `investigation_log` to `[]`.
4. Read [../references/investigation-log.md](../references/investigation-log.md).
5. Do not invent fields that the schema does not list.

## Step 2 — Intake (required)

1. Run Screen A: is this **analysis**?
2. If no, set `mode: skip` and stop this skill.
3. If yes, run Screen B signals.
4. Record `place` when the work sits in a required-investigation context (see [../references/thorough-investigation.md](../references/thorough-investigation.md)).
5. Set `mode` to `loop` or `full_graph`.
6. Write `intake` into state and append an investigation_log hop for intake.
7. Do not start `problem-framer` until intake is done.

## Step 3 — Choose path from intake

1. If `mode: loop`, pick one specialty from [../diagrams/checklist-router.mmd](../diagrams/checklist-router.mmd).
2. If `mode: full_graph`, follow [../diagrams/analysis-agent-graph.mmd](../diagrams/analysis-agent-graph.mmd) from `problem-framer`.
3. If more than one checklist trigger is true and Screen A passed, prefer **full_graph**.

## Step 4 — Route each hop

1. Load [../agents/orchestrator.md](../agents/orchestrator.md) when you need a router.
2. Read diagrams for `default_next` and re-entry edges.
3. Write `routing_notes` with `next_agent`, `heuer_lines`, `default_next`, `consult`.
4. Load the matching file under [../agents/](../agents/).
5. Do only that agent job.
6. Write only the fields that agent owns.
7. If stuck, read only the handed `heuer_lines` from the book. Never other chapters.
8. When verify passes, append one `investigation_log` entry.
9. Then hand off. Orchestrator refuses handoff if the prior hop has no log entry.
10. A `consult` agent is a short helper pass. Log it as its own hop.

## Step 5 — Full graph extras

1. Run `skeptical-reviewer` before you treat the ranking as final.
2. Optional `consult` agents do not skip the main path.
3. Write `problem` only after `problem-framer`.

## Step 6 — Build the ACH matrix

1. Use [../references/ach-template.md](../references/ach-template.md).
2. Use [../diagrams/ach-evidence-matrix.mmd](../diagrams/ach-evidence-matrix.mmd) as the picture of the work.
3. Mark each cell `C`, `I`, `N`, or `?`.
4. Rank by hard `I` marks first. Do not rank by count of `C` marks.
5. Run [../references/matrix-completeness.md](../references/matrix-completeness.md) before you leave evaluator.
6. If any cell is missing, fill it. Do not hand a holey matrix to selector-reporter.

## Step 7 — Read Heuer text (only if stuck)

1. Open [../references/source.md](../references/source.md).
2. Read only the line range for the current agent.
3. Do not load the full book file into context.

## Step 8 — Report

1. State all live hypotheses with odds or ranges.
2. State why you reject each rejected hypothesis.
3. List milestones that change the odds.
4. Keep rejected hypotheses as receipts.

## Step 9 — After a miss

1. Load `learner-postmortem`.
2. Judge the process with the data that existed at decision time.
3. Write one durable lesson into your notes or into this skill.

## Hard rules

1. Never load the full Heuer book into the prompt.
2. Never skip intake.
3. Never run full graph on pure implement / explain-code / clear-repro debug work.
4. Never confirm a favorite story and stop.
5. Never say "there is no evidence" without a check that evidence can be seen if true.
6. Never skip `skeptical-reviewer` in full-graph mode.
7. Write clear full sentences in reports. Do not use telegram fragments.
8. Obey orchestrator spend caps in [../agents/orchestrator.md](../agents/orchestrator.md).
9. Meet the quality bar in [effectiveness.md](effectiveness.md) before you call the analysis done.
