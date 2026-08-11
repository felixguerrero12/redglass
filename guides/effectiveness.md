# Effectiveness (for agents)

This guide states what makes this skill work. Use it with [how-to-use.md](how-to-use.md).

## Goal

Raise the chance of a correct call under incomplete data.
Do not optimize for long runs or many agents.

## Highest-leverage moves

1. Write the problem before you collect.
2. Force more than one live hypothesis before you evaluate.
3. Work **inconsistencies** in the matrix. Do not crown the hyp with the most `C` marks.
4. Keep unproven hyps alive until disproved. This includes deception when relevant.
5. Run `skeptical-reviewer` in full-graph mode. Do not self-approve the ranking.
6. Pre-specify milestones. Treat surprise as a signal.
7. Obey orchestrator spend caps. A bounded graph beats an endless one.
8. Never hand off a holey matrix. Run [../references/matrix-completeness.md](../references/matrix-completeness.md).
9. Append an `investigation_log` entry after every hop before the next handoff.

## Cheap checks that catch expensive errors

| Symptom | Consult or run |
|---|---|
| One "obvious" story | `hypothesis-generator` |
| Confirming-data pile | `collector` + `bias-guard` |
| Ignoring minuses | `evaluator` |
| "No evidence that…" | `bias-guard` |
| Mirror-imaging | `open-mind` |
| Soft odds, hidden rejects | `selector-reporter` then `skeptical-reviewer` |
| Prose table ≠ YAML matrix | `evaluator` + matrix-completeness check; reviewer must fail |

## What not to do

1. Do not load the full Heuer book.
2. Do not skip diagrams when you choose `default_next`.
3. Do not use `consult` to avoid the main path.
4. Do not treat absence of evidence as disproof when concealment is plausible.
5. Do not spend the review-fail budget on wording nits. Spend it on diagnostic gaps.
6. Do not rank or pass review on an incomplete matrix.

## Quality bar for a finished report

1. Problem statement is explicit.
2. At least two hyps were live during evaluation (unless one was disproved early with hard `I` evidence).
3. Matrix shows diagnostic marks, not only `C`.
4. Matrix passes [../references/matrix-completeness.md](../references/matrix-completeness.md).
5. Odds or ranges appear on the key call.
6. Rejected hyps have reasons.
7. Milestones are listed.
8. Reviewer pass exists in full-graph mode (or residual risk is stated after cap breach).
9. `investigation_log` has one entry per hop in order.

See worked example: [../examples/service-outage-ach.md](../examples/service-outage-ach.md).
Skip / loop intake: [../examples/skip-loop-intake.md](../examples/skip-loop-intake.md).
Self-review dogfood: [../examples/skill-self-review-ach.md](../examples/skill-self-review-ach.md).
Smoke (matrix miss): [../examples/smoke-auth-pr-ach.md](../examples/smoke-auth-pr-ach.md).
Resmoke (matrix pass): [../examples/smoke-auth-pr-resmoke.md](../examples/smoke-auth-pr-resmoke.md).
Investigation log example: [../examples/investigation-log-auth-pr.md](../examples/investigation-log-auth-pr.md).
Required inputs gate: [../references/required-inputs.md](../references/required-inputs.md).
Matrix completeness: [../references/matrix-completeness.md](../references/matrix-completeness.md).
Investigation log schema: [../references/investigation-log.md](../references/investigation-log.md).
