# Diagrams

First-class Mermaid sources. These files are **directions**, not decoration.
The orchestrator must read them before each handoff.

| File | Direction use |
|---|---|
| [modes-and-loops.mmd](modes-and-loops.mmd) | skip / loop / full_graph overview + mid-run raise |
| [analysis-agent-graph.mmd](analysis-agent-graph.mmd) | `default_next` path + labeled re-entry edges |
| [checklist-router.mmd](checklist-router.mmd) | Trigger → entry agent |
| [ach-evidence-matrix.mmd](ach-evidence-matrix.mmd) | How evidence links to hyps (ACH picture) |
| [campaign-build.mmd](campaign-build.mmd) | Repo build DAG (ops only) |

Agents: [`../agents/`](../agents/).
Orchestrator rules: [`../agents/orchestrator.md`](../agents/orchestrator.md).
