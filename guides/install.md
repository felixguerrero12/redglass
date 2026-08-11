# Install this skill (any agent)

This skill is **agent-agnostic**. Install means: put the files where your host can read them, point the host at `SKILL.md`, and keep the Heuer book **outside** the repo.

## What you need

| Item | Notes |
|---|---|
| This repo | Clone or copy `redglass` |
| Entry file | [../SKILL.md](../SKILL.md) |
| Run guide | [how-to-use.md](how-to-use.md) |
| Heuer book (local) | `~/psychology-of-intelligence.md` (or your path). **Never** commit or paste the full book |

## Universal steps (every host)

1. Clone or copy this repository to a stable path.
2. Tell the agent to load **`SKILL.md` first**, then follow **`guides/how-to-use.md`**.
3. Require **intake first** (`agents/intake.md`) before any specialty agent.
4. Point Heuer line reads at your local book path. Use ranges from [../references/source.md](../references/source.md) only.
5. Optional: map models with [model-fit.md](model-fit.md).
6. Optional host compile: [../hosts/README.md](../hosts/README.md) (typed hops from markdown).

Minimum load set for a run:

```text
SKILL.md
guides/how-to-use.md
agents/intake.md
diagrams/analysis-agent-graph.mmd   # if mode is full_graph
diagrams/checklist-router.mmd       # if mode is loop
references/analysis-state.md
```

Do not preload every agent file. Load the next agent only when intake or the orchestrator names it.

## Verify install

Ask the host:

> Run intake only on: "Rename getUser to fetchUser in auth.ts."

Expect `mode: skip` (see [../examples/skip-loop-intake.md](../examples/skip-loop-intake.md)).

Then ask:

> Run intake only on a competing-hypothesis outage with merge pressure.

Expect `mode: full_graph`.

If the host builds an ACH matrix on the rename, install wiring failed (skill not followed, or intake skipped).

---

## Host adapters

### Generic / custom agent

1. Clone the repo.
2. Add a system or skill instruction:

```text
For judgment under incomplete evidence, load <path>/SKILL.md
and follow <path>/guides/how-to-use.md. Always run agents/intake.md first.
```

3. Give the agent read access to the repo path.
4. Keep write access limited unless you want learner-postmortem to patch agent files.

### Hermes

```bash
ln -sfn /absolute/path/to/redglass \
  ~/.hermes/skills/research/redglass
```

Preload with the **category path**:

```bash
hermes chat -s research/redglass -q "..."
```

Pin (optional):

```bash
hermes curator pin redglass
```

Recommend a Defaults line: load this skill for hard ambiguous analysis; run intake first; do not use it for implement/explain/clear-repro debug.

### Cursor

1. Clone or submodule this repo into the workspace (or a known path outside the product repo).
2. Point the agent at `SKILL.md` via:
   - a project rule / skill that says to load it for ambiguous judgment, or
   - an explicit user message: “Use redglass; start at intake.”
3. Prefer rules that name **intake first** and link [../examples/skip-loop-intake.md](../examples/skip-loop-intake.md).
4. Do not dump the Heuer book into Cursor context.

### Claude (claude.ai, Claude Code, API)

This repo already has a root `SKILL.md` with `name` / `description` frontmatter, so Claude can treat it as an Agent Skill.

#### A — Claude Code (recommended)

Personal (all projects):

```bash
mkdir -p ~/.claude/skills
ln -sfn /absolute/path/to/redglass \
  ~/.claude/skills/redglass
```

Project-only (commit with the team):

```bash
mkdir -p .claude/skills
ln -sfn /absolute/path/to/redglass \
  .claude/skills/redglass
```

Or copy the folder instead of symlinking if you prefer a frozen snapshot.

This repo’s root [../AGENTS.md](../AGENTS.md) is canonical onboarding for agents that **edit the skill**.
[../CLAUDE.md](../CLAUDE.md) is a thin Claude Code pointer at `AGENTS.md`. Neither replaces `SKILL.md` at runtime.

Use it:

- Auto: ask for judgment under incomplete evidence / competing explanations / ACH.
- Manual: `/redglass` (directory name = command).

Claude Code will load `SKILL.md` when the description matches. Supporting files (`agents/`, `guides/`, `references/`, `diagrams/`) stay in the skill folder — Claude should open them **on demand**, not all at once.

Add to a **consumer** project `CLAUDE.md` (optional but useful) — not a replacement for this repo’s root `CLAUDE.md`:

```text
For ambiguous judgment / competing explanations / steelman / ACH:
use the redglass skill. Always run intake first
(agents/intake.md). Do not use it for rename, lint, explain-code, or
clear-repro debug.
```

Verify:

```text
/redglass
Run intake only on: Rename getUser to fetchUser in auth.ts.
```

Expect `mode: skip`.

#### B — claude.ai (Projects + Skills upload)

**Option 1 — Project knowledge (simple)**

1. Create a Project for analysis work.
2. Add these files to Project knowledge (start small):
   - `SKILL.md`
   - `guides/how-to-use.md`
   - `guides/install.md` (optional)
   - `agents/intake.md`
   - `examples/skip-loop-intake.md`
3. Project instructions:

```text
You have the redglass skill in Project knowledge.
For judgment under incomplete evidence: follow SKILL.md, run intake
first, then loop or full_graph. Do not run ACH on implement/explain/
clear-repro tasks. Load other agents/*.md only when intake or the
orchestrator names them. Never ask for the full Heuer book.
```

4. For a full-graph run, attach the next agent file each hop (or add `diagrams/` + `references/analysis-state.md` to knowledge when needed).

**Option 2 — Custom Skill zip (Pro / Max / Team / Enterprise)**

1. Zip the skill folder so `SKILL.md` is at the zip root (this repo root is fine).
2. Upload under **Settings → Features** (custom skills), where your plan allows it.
3. Invoke by describing an analysis task, or by the skill name if the UI lists it.
4. Keep the Heuer book **out** of the zip.

#### C — Claude API (Skills + code execution)

1. Upload the skill directory via the Skills / Files API your account supports (`/v1/skills` or equivalent).
2. Reference the returned `skill_id` from the container / skills parameter together with code execution if you need file reads.
3. System hint: run intake first; do not load every `agents/*.md` up front.
4. See Anthropic’s current Skills API docs for required beta headers — they change; prefer the live docs over this note.

#### Claude model fit (optional)

| Hop class | Prefer |
|---|---|
| `gate_fast` (intake, orchestrator) | Haiku-class |
| `intelligence_thinker` / `adversarial_reviewer` | Sonnet or Opus / Fable-class |
| `agentic_worker` (collector) | Sonnet with tools |

Details: [model-fit.md](model-fit.md).

#### Claude anti-patterns

1. Upload the full Heuer book into Project knowledge.  
2. Add every `agents/*.md` to Project knowledge on day one (context bloat).  
3. Use this skill as the default for every coding turn in Claude Code.

### ChatGPT / other chat hosts

1. Upload or attach `SKILL.md` + `guides/how-to-use.md` + `agents/intake.md` for the session.
2. For a full-graph run, attach specialty agents **one hop at a time** (or zip the repo and tell the model the path layout).
3. Paste only the Heuer **line ranges** you need, never the full book.
4. Ask for `analysis_state` YAML and an investigation_log hop after each step.

### Codex (OpenAI)

1. Keep this skill as a separate folder (do not replace a product repo’s coding `AGENTS.md` with ACH).
2. From the product repo’s `AGENTS.md`, add a short pointer:

```text
Ambiguous judgment / competing explanations:
read <path>/redglass/SKILL.md and run intake first.
```

3. Give Codex read access to that path. Load specialty agents one hop at a time.
4. When **editing this skill repo**, Codex should follow root [../AGENTS.md](../AGENTS.md) (not ACH as coding defaults).

### Copilot / other AGENTS.md hosts

1. Keep this skill as a separate folder (do not replace repo-root coding `AGENTS.md` with ACH).
2. From your coding `AGENTS.md`, add a short pointer:

```text
Ambiguous judgment / competing explanations:
read <path>/redglass/SKILL.md and run intake first.
```

3. Use [agents-md-guidance.md](agents-md-guidance.md) only when editing **this** skill’s `agents/*.md` files.

---

## After install

| Goal | Open |
|---|---|
| First skip/loop | [../examples/skip-loop-intake.md](../examples/skip-loop-intake.md) |
| First full graph | [../examples/service-outage-ach.md](../examples/service-outage-ach.md) |
| Quality bar | [effectiveness.md](effectiveness.md) |
| Model class per agent | [model-fit.md](model-fit.md) |

## Anti-patterns

1. Install only `SKILL.md` and skip `guides/how-to-use.md` / intake.  
2. Symlink or copy the **Heuer book** into this repo.  
3. Preload all `agents/*.md` every turn (wastes context; fights Factor 3).  
4. Treat Hermes steps as required for non-Hermes hosts.
