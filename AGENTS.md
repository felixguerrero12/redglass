# AGENTS.md — redglass

Short onboarding for coding agents that **edit this repo**.
Runtime ACH instructions live in `SKILL.md`, not here.

Host install (Hermes, Cursor, Claude, Codex, …) lives in `guides/install.md` — not in this file.

## WHY

This repo ships an **agent-agnostic skill** for judgment under incomplete evidence
(Heuer checklist + ACH + specialty agents). Hermes/Claude/Cursor/Codex are hosts, not the product.

## WHAT

| Path | Role |
|---|---|
| `SKILL.md` | Skill entry (intake gate, roster) |
| `agents/` | Specialty agent SOPs (markdown = source of truth) |
| `guides/` | how-to-use, install, effectiveness, model-fit, agents-md-guidance |
| `diagrams/` | Mermaid directions (`.mmd`) — trust these for `default_next` |
| `references/` | State schema, ACH template, Heuer line index, gates |
| `examples/` | Worked skip/loop/full-graph and smoke notes |
| `hosts/` | Optional typed-hop compile from `agents/*.md` |
| `research/` | Background maps (not runtime) |

Never commit or paste the full Heuer book. Local path: `~/psychology-of-intelligence.md`.
Line ranges only: `references/source.md`.

## HOW

1. Read `guides/install.md` before changing host-adapter docs.
2. Edit agents with `guides/agents-md-guidance.md` (Tools/checks, Boundaries, Output example).
3. Prose: `STYLE.md` (simple technical English).
4. After changing an agent’s frontmatter or **Next agents** table:

```bash
python3 hosts/compile_agent_hop.py agents/<id>.md
python3 hosts/compile_agent_hop.py --check agents/<id>.md
# or all agents:
python3 hosts/compile_agent_hop.py --all
python3 hosts/compile_agent_hop.py --check --all
```

5. Prefer the cheapest correct change. Do not invent new specialty agents without a real miss.
6. Do not replace owned markdown agents with opaque `role/goal/personality` wrappers.

## Progressive disclosure (read when needed)

| Need | Open |
|---|---|
| Run the skill | `SKILL.md` → `guides/how-to-use.md` → `agents/intake.md` |
| Install on a host | `guides/install.md` |
| Model class per agent | `guides/model-fit.md` |
| Skip vs loop vs full graph | `examples/skip-loop-intake.md` |
| Full-graph example | `examples/service-outage-ach.md` |
| Agent file quality | `guides/agents-md-guidance.md` |
| 12-factor mapping | `research/12-factor-agents-mapping.md` |

## Do not put here

- Full ACH checklists (those belong in `agents/` / `SKILL.md`)
- Host-adapter install steps (see `guides/install.md`)
- Long style essays (see `STYLE.md`)
- Heuer chapter text
- Every shell command you might ever run
