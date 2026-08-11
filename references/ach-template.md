# ACH matrix template

Use for Analysis of Competing Hypotheses. Fill in normal clear prose (not caveman fragments).

## Setup

```yaml
problem: string                 # question being judged
mind_set_assumptions: [string]  # explicit lenses / priors
hypotheses:
  - id: H1
    statement: string
  - id: H2
    statement: string
  # include deception/concealment hyp when relevant
evidence:
  - id: E1
    claim: string
    source_reliability: high|medium|low|unknown
    notes: string
```

## Matrix

For each evidence × hypothesis cell: `C` consistent · `I` inconsistent · `N` neutral/irrelevant · `?` unknown

| Evidence | H1 | H2 | H3 | diagnostic? |
|---|---|---|---|---|
| E1 |  |  |  | yes/no |
| E2 |  |  |  | yes/no |

Diagnostic = discriminates among hypotheses (not consistent with almost all).

## Scoring (tentative)

Work **inconsistencies** first:

```yaml
ranking_notes: |
  Hypotheses with fewest hard inconsistencies tend to be most likely.
  Do not crown the hyp with the most "consistent" marks.
sensitivity:
  linchpins: [string]           # evidence/assumptions that swing the call
  if_wrong: string              # what changes if they fail / are deceptive
relative_likelihood:
  - {id: H1, odds_or_range: "e.g. 55-70%", why: string}
  - {id: H2, odds_or_range: string, why: string}
rejected:
  - {id: H3, why: string}       # keep as receipts
milestones:
  - string                      # observations that would change probabilities
open_collection:
  - string                      # what to seek next to refute remaining hyps
```

## Report shape

1. Question + explicit assumptions  
2. Hypotheses considered  
3. Key diagnostic evidence (and what was non-diagnostic)  
4. Relative likelihoods + uncertainty  
5. Why alternatives were rejected  
6. Milestones to watch  
