# 12-Factor Agents mapping

Comparative note for this skill.
Source: [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents) (Dex Horthy / HumanLayer).
License of their content: CC BY-SA 4.0.

This skill is a **markdown SOP / agent graph**, not a production agent runtime.
Use these factors as design checks. Do not pull in their framework.

## Factor map

| Factor | Name | Fit for this skill | Our practice |
|---|---|---|---|
| 1 | Natural language → tool calls | Host concern | Hosts turn user asks into intake + specialty hops |
| 2 | Own your prompts | **Strong** | Each `agents/*.md` is the owned prompt/SOP. No black-box role/goal/personality wrapper |
| 3 | Own your context window | **Strong** | Heuer by line slice only. Shared `analysis_state`. Caps on slice reads |
| 4 | Tools are structured outputs | Medium | YAML state writes + Output examples. Hosts can harden to schemas later |
| 5 | Unify execution + business state | **Strong** | One `analysis_state` + `investigation_log` |
| 6 | Launch / pause / resume APIs | Host / future | `Ask first` boundaries + saved state enable pause; no HTTP API in-repo |
| 7 | Contact humans with tool calls | Soft | Boundaries **Ask first**; high-stakes places in thorough-investigation |
| 8 | Own your control flow | **Strong** | Intake gate; diagrams as directions; spend caps; re-entry edges |
| 9 | Compact errors into context | Soft | Reviewer issues stay short and actionable |
| 10 | Small, focused agents | **Strong** | One job per agent. Selector ≠ reviewer |
| 11 | Trigger from anywhere | Host | Any host that can load `SKILL.md` |
| 12 | Stateless reducer | Soft / good target | Each hop: state in → owned writes → log → handoff |

Honorable mention (their appendix 13): pre-fetch context you might need — we pre-declare Heuer slices and required inputs instead of dumping the book.

## Why Factor 2 matters here

Their anti-pattern:

```text
Agent(role=..., goal=..., personality=..., tools=[...])
Task(instructions=..., expected_output=...)
```

That hides the real tokens. Tuning becomes reverse-engineering the framework.

Their preferred style (owned prompt + typed next step):

```text
DetermineNextStep(thread) ->
  DoneForNow | ListGitTags | DeployBackend | RequestMoreInformation

# full system + user prompt owned in code
# "What should the next step be?"
```

See [factor-02-own-your-prompts.md](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-02-own-your-prompts.md).

### Is that style interesting for us?

Yes. We already do the important half:

1. **Own the text** — specialty agents are first-class files under `agents/`.
2. **No framework black box** — hosts load our markdown; we do not hide prompts inside Crew/LangChain wrappers.
3. **Typed-ish next steps** — `routing_notes` names `next_agent`, `default_next`, `consult` from an owned graph.

What Factor 2 adds as a **host pattern** (optional, later):

| Their idea | Host adaptation |
|---|---|
| Prompt as code | Compile `agents/<id>.md` into the system message for that hop |
| Union of next intents | Orchestrator returns only legal edges from `analysis-agent-graph.mmd` |
| Evals on prompts | Smoke ACH examples as golden fixtures |
| Full token control | Never let a framework rewrite Summary / Boundaries / Output example |

Do **not** replace our markdown agents with opaque `role/goal/personality` objects.
If a host wants BAML-style functions, generate them **from** our agent files so the markdown stays the source of truth.

### Sketch (host-side)

Implemented under [`../hosts/`](../hosts/):

```bash
python3 hosts/compile_agent_hop.py agents/evaluator.md
```

That compiles `agents/evaluator.md` → typed hop modules in `hosts/generated/`
(`evaluator_hop.py` + `evaluator_hop.ts`).

```text
RunEvaluator(state) -> BiasGuard | OpenMind | Collector | ProblemFramer

system: full contents of agents/evaluator.md   # owned prompt
user: required analysis_state fields only
constraint: next_agent ∈ LEGAL_NEXT from ## Next agents
```

Markdown stays the source of truth. Re-run the compiler after agent edits.
Use `--check` in CI to catch stale generated hops.

## Factor 10 reminder

Small focused agents beat one mega-loop.
Our intake gate exists so hosts do **not** run the full graph on every chat.
Spend caps exist so context does not grow until the model gets lost.

## What we will not do from that repo

1. Adopt HumanLayer / kubechain / BAML as a dependency of this skill.
2. Turn analysis into an unbounded tool-loop with a bag of tools.
3. Hide Heuer method inside a framework prompt template.

## Related in this repo

- [../guides/agents-md-guidance.md](../guides/agents-md-guidance.md) — how we write owned agent files
- [../guides/model-fit.md](../guides/model-fit.md) — which model class runs each owned prompt
- [../agents/orchestrator.md](../agents/orchestrator.md) — owned control flow
- [agent-practice-board.md](agent-practice-board.md) — Heuer-grounded craft behind each agent
