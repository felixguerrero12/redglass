# Agent file guidance

How to write specialty agents for this skill.
Adapted from GitHub’s lessons on `agents.md` files
([How to write a great agents.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/), Nov 2025).

## What transfers

GitHub found that vague helpers fail.
Specialists with a clear job, early commands, examples, and hard boundaries work.

That transfers here:

| GitHub lesson | Do this here |
|---|---|
| Specific persona | One job per file. Name it in the one-liner and `description`. |
| Commands early | Put **Tools / checks** near the top. Name concrete steps and paths. |
| Examples over prose | Show a short good YAML write. Add one bad anti-example when useful. |
| Clear boundaries | Use **Always / Ask first / Never**. |
| Stack + structure | Name Heuer line slices, state fields, and key reference paths. |

## What does not transfer

These files are **analysis SOP nodes**, not GitHub Copilot coding personas.

| Copilot pattern | Why we skip or adapt it |
|---|---|
| `npm test` / build commands | No app build. Use matrix gates, log hops, and templates instead. |
| React / Vite stack versions | Domain stack is Heuer method + `analysis_state`. |
| Git commit workflow | Default handoff is log → route → next agent. Git only when you patch skill files. |
| Write only under `tests/` | Writes go into shared `analysis_state` fields this agent owns. |

## Adapted six core areas

| GitHub area | This skill |
|---|---|
| Commands | **Tools / checks** (template, completeness gate, append log) |
| Testing | **Verify / stop** before handoff |
| Project structure | **State** inputs/writes + `references/` / `diagrams/` paths |
| Code style | STE ([STYLE.md](../STYLE.md)) + **Output example** |
| Git workflow | **Handoff workflow** (log → `routing_notes` → `default_next`) |
| Boundaries | **Always / Ask first / Never** |

## Contract (section order)

After frontmatter, keep this order:

1. Title + one-liner
2. Summary (persona)
3. Model fit
4. Tools / checks (early)
5. Best practices
6. Boundaries (Always / Ask first / Never)
7. Output example
8. State (inputs / writes / verify)
9. Next agents

### Frontmatter fields

```yaml
id: agent-id                 # canonical
description: one sentence    # discoverability
checklist_step: string
load_when: string
heuer_lines: [ranges]
version: x.y.z
model_class: gate_fast | balanced_mid | intelligence_thinker | agentic_worker | adversarial_reviewer
model_examples: string
model_avoid: string
```

## Pass / fail checklist

A specialty agent file is good when all are true:

1. Persona is specific. A reader can say what it does and does not do.
2. Tools / checks appear before long best-practice lists.
3. At least one good **Output example** matches the fields it writes.
4. Boundaries use three tiers (Always / Ask first / Never).
5. Never list includes: invent state, steal another agent’s job, load the full Heuer book.
6. Verify / stop is testable without vibes.
7. Next agents match [../diagrams/analysis-agent-graph.mmd](../diagrams/analysis-agent-graph.mmd) for `default_next`.
8. Prose follows [../STYLE.md](../STYLE.md).
9. Model fit is present. See [model-fit.md](model-fit.md).

## Gold exemplar

Use [../agents/evaluator.md](../agents/evaluator.md) as the craft exemplar.
Copy its shape. Keep other agents shorter when their job is thinner.

## Related

- [model-fit.md](model-fit.md) — which model class to run
- [../research/12-factor-agents-mapping.md](../research/12-factor-agents-mapping.md) — own-your-prompts and small-agent factors
- [../agents/README.md](../agents/README.md) — roster
- [effectiveness.md](effectiveness.md) — quality bar
