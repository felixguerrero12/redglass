# Host adapters (optional)

This folder is **not** required to use the skill.
Any host can load `SKILL.md` and `agents/*.md` directly.

What lives here: optional compile helpers so a runtime can treat each agent file as an owned prompt with a **typed next-hop union** (12-Factor Agents, Factor 2).

## Rule

**Markdown under `agents/` is the source of truth.**
Generated hops must be regenerable. Do not edit generated files by hand.

## Compile one agent

```bash
python3 hosts/compile_agent_hop.py agents/evaluator.md
```

## Compile every agent

```bash
python3 hosts/compile_agent_hop.py --all
python3 hosts/compile_agent_hop.py --check --all
```

Writes one `*_hop.py` + `*_hop.ts` pair per `agents/*.md` with an `id`.
The next-agent id `idle` means stop (no further specialty hop).

Writes:

- `hosts/generated/evaluator_hop.py` — typed hop module
- `hosts/generated/evaluator_hop.ts` — TypeScript twin (types + prompt loader sketch)

## Use the hop (Python sketch)

```python
from hosts.generated.evaluator_hop import (
    load_prompt,
    build_user_payload,
    parse_next_hop,
    LEGAL_NEXT,
)

system = load_prompt()                 # full agents/evaluator.md
user = build_user_payload(state)       # only required inputs
# ... call your LLM with system + user ...
next_hop = parse_next_hop(llm_json)  # raises if next_agent not in LEGAL_NEXT
```

## Regenerating

Re-run the compiler after you change an agent’s frontmatter or **Next agents** table.

```bash
python3 hosts/compile_agent_hop.py agents/evaluator.md
python3 hosts/compile_agent_hop.py --check agents/evaluator.md  # exit 1 if stale
python3 hosts/compile_agent_hop.py --all
python3 hosts/compile_agent_hop.py --check --all
```
