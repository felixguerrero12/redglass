# Model fit per agent

This skill is **agent-agnostic**. Hosts still pick a model (or worker class) per node.
Wrong fit wastes money or weakens judgment.

Each agent file also has a **Model fit** section and `model_class` in its frontmatter.
Persona, Tools/checks, Boundaries, and Output examples live in each agent file.
See [agents-md-guidance.md](agents-md-guidance.md) for the file contract.
This guide is the full model table and pairing advice.

This guide names **capability classes**, then maps **example models**.
Examples use common Cursor-era names. Other hosts can map the same classes.

## Capability classes

| Class | Job shape | Prefer when |
|---|---|---|
| `gate_fast` | Classify, route, enforce a short checklist | High volume, low ambiguity, must stay cheap |
| `balanced_mid` | Solid judgment, clear prose, moderate depth | Default analysis hop when stakes are medium |
| `intelligence_thinker` | Compete hyps, stress linchpins, fight mind-set | High ambiguity or high cost of error |
| `agentic_worker` | Tool loops, dig, verify files, fetch evidence | Collection and fact-finding dominate |
| `adversarial_reviewer` | Fail closed on another agent's work | Must not share the producer's blind spots |

### Example model map (illustrative)

| Class | Lighter / faster | Mid | Deeper thinker |
|---|---|---|---|
| `gate_fast` | Haiku, Composer 2.5 fast | Grok (fast tier) | — |
| `balanced_mid` | Sonnet (standard) | Grok 4.5, Composer 2.5 | Sonnet thinking |
| `intelligence_thinker` | Sonnet thinking | Grok high | Fable, Opus |
| `agentic_worker` | Composer 2.5 | Grok, Sonnet + tools | Fable only if dig is hard |
| `adversarial_reviewer` | Sonnet (other than producer) | Grok | Fable or Opus |

Rules:

1. Prefer **class fit** over brand loyalty.
2. Do not put a pure coding agent on mind-set work if a thinker is available.
3. Do not put a max thinker on intake for every chat. That burns budget.
4. For `skeptical-reviewer`, prefer a **different model family** than `selector-reporter`.

## Fit by specialty agent

| Agent | Class | Why | Good examples | Avoid |
|---|---|---|---|---|
| `intake` | `gate_fast` | Screen A/B is classification. Must be reliable and cheap. | Haiku, Composer 2.5, Grok fast | Fable/Opus on every request |
| `orchestrator` | `gate_fast` | Caps, handoff verify, log gate. Structure over poetry. | Haiku, Composer 2.5, Grok fast | Deep thinker that rewrites ACH |
| `problem-framer` | `intelligence_thinker` | Wrong question wastes the whole graph. | Sonnet thinking, Fable | Haiku alone on muddy scope |
| `hypothesis-generator` | `intelligence_thinker` | Satisficing kills the set. Needs breadth under uncertainty. | Sonnet thinking, Fable, Grok high | Tiny models that keep one story |
| `collector` | `agentic_worker` | Dig, fetch, log gaps, seek mind-changers. | Composer 2.5, Grok, Sonnet + tools | Pure chat model with no tools |
| `evaluator` | `intelligence_thinker` | ACH matrix and diagnosticity are the core craft. | Sonnet thinking, Fable, Opus | Fast coding-only models |
| `bias-guard` | `balanced_mid` | Checklist audit. Needs care, not invention. | Sonnet, Grok | Models that invent new hyps here |
| `open-mind` | `intelligence_thinker` | Mind-set and mirror-imaging need depth. | Fable, Sonnet thinking | Haiku; coding-only Composer |
| `selector-reporter` | `balanced_mid` → thinker if stakes high | Odds, reject receipts, clear report. | Sonnet, Grok; Fable if high stakes | Haiku for high-cost calls |
| `skeptical-reviewer` | `adversarial_reviewer` | Fail closed. Prefer **not** the same model as selector. | Fable/Opus if selector was Sonnet; Sonnet if selector was Composer | Same model + same prompt stack as selector |
| `monitor` | `gate_fast` or `balanced_mid` | Milestone list and surprise triage. | Haiku, Composer 2.5, Sonnet | Max thinker for routine watches |
| `learner-postmortem` | `intelligence_thinker` | Fair process review. Hindsight traps are strong. | Sonnet thinking, Fable | Fast models that rewrite history |

## Suggested pairing for a full graph

Cheap default path (good enough for many runs):

| Hop | Example |
|---|---|
| intake + orchestrator | Haiku or Composer 2.5 |
| problem-framer → open-mind | Sonnet thinking |
| collector | Composer 2.5 or Grok |
| selector-reporter | Sonnet |
| skeptical-reviewer | Fable or Opus (different from selector) |
| monitor | Haiku or Composer 2.5 |

High-stakes path (security, merge gate, motive, postmortem):

| Hop | Example |
|---|---|
| intake | Sonnet (still gate, but stricter) |
| framing → evaluation → open-mind | Fable or Opus |
| collector | Composer 2.5 or Grok with tools |
| selector + reviewer | Two different deep thinkers |

## Single-model hosts

If the host can run only one model for the whole graph:

1. Prefer a **balanced mid thinker** (Sonnet-class) over a coding-only agentic model.
2. Still run intake first.
3. Still run skeptical-reviewer as a **separate pass** with a fresh prompt (adversarial role), even on the same model.
4. Raise to a deeper model only when [thorough-investigation.md](../references/thorough-investigation.md) triggers fire.

## What this is not

1. Not a rank of which company is “best.”
2. Not a requirement to use Cursor models.
3. Not permission to skip intake to save tokens.

## Related

- [thorough-investigation.md](../references/thorough-investigation.md) — when to spend deeper models
- [effectiveness.md](effectiveness.md) — quality bar
- [../agents/orchestrator.md](../agents/orchestrator.md) — spend caps still apply
