# Source — checklist router + book section slices

Richards J. Heuer, Jr., *Psychology of Intelligence Analysis* (CSI/CIA, 1999).

PDF: https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf

This skill teaches method. It does not put the full book into the prompt.

**Primary path:** section files under [`../book/`](../book/) (see also [`../book/00-index.md`](../book/00-index.md)). Rebuilt from the CIA PDF on 2026-08-11.

Optional legacy monolith (local OCR copy only; do not use as the primary Read path): `~/psychology-of-intelligence.md`.

## How to read

Never load the entire book. Do not `cat` or Read all of `book/`.

1. Walk the agent checklist in [../SKILL.md](../SKILL.md).
2. If you need Heuer text, open **only** the linked section file for that agent (Read tool on that path).
3. Usual max: **one** section file per hop. Rarely two short sections.
4. Do not open chapter files and agent files for the same hop unless the router names both.

## Agent → section files

| Agent | Section file | Contents |
|---|---|---|
| problem-framer | [problem-framer.md](../book/problem-framer.md) | Ch 7 + Ch 14 define-problem checklist |
| hypothesis-generator | [hypothesis-generator.md](../book/hypothesis-generator.md) | Ch 4 + Ch 8 through Step 1 / outline |
| collector | [collector.md](../book/collector.md) | Ch 5 (+ Ch 14 collecting checklist) |
| evaluator | [evaluator.md](../book/evaluator.md) | Full Ch 8 |
| selector-reporter | [selector-reporter.md](../book/selector-reporter.md) | Full Ch 8 |
| monitor | [monitor.md](../book/monitor.md) | Ch 8 Step 8 + Ch 14 monitoring |
| bias-guard | [bias-guard.md](../book/bias-guard.md) | Ch 10 |
| open-mind | [open-mind.md](../book/open-mind.md) | Ch 2 + Ch 6 |
| learner-postmortem | [learner-postmortem.md](../book/learner-postmortem.md) | Full Ch 13 |

Full checklist text also sits in Ch. 14 ([ch14-improving-analysis.md](../book/ch14-improving-analysis.md)).

## Appendix: chapter catalog

Optional non-agent lookups (same one-or-two-files rule):

| Section | File |
|---|---|
| Front matter / TOC | [front-matter.md](../book/front-matter.md) |
| Author's Preface | [authors-preface.md](../book/authors-preface.md) |
| Foreword (MacEachin) | [foreword.md](../book/foreword.md) |
| Introduction (Davis) | [introduction.md](../book/introduction.md) |
| Ch 1 Thinking | [ch01-thinking.md](../book/ch01-thinking.md) |
| Ch 2 Perception | [ch02-perception.md](../book/ch02-perception.md) |
| Ch 3 Memory | [ch03-memory.md](../book/ch03-memory.md) |
| Ch 4 Strategies | [ch04-strategies.md](../book/ch04-strategies.md) |
| Ch 5 More Info? | [ch05-more-info.md](../book/ch05-more-info.md) |
| Ch 6 Open Mind | [ch06-open-mind.md](../book/ch06-open-mind.md) |
| Ch 7 Structuring | [ch07-structuring.md](../book/ch07-structuring.md) |
| Ch 8 ACH | [ch08-ach.md](../book/ch08-ach.md) |
| Ch 9 Cognitive Biases | [ch09-cognitive-biases.md](../book/ch09-cognitive-biases.md) |
| Ch 10 Evidence biases | [ch10-evidence-biases.md](../book/ch10-evidence-biases.md) |
| Ch 11 Cause and Effect | [ch11-cause-and-effect.md](../book/ch11-cause-and-effect.md) |
| Ch 12 Probabilities | [ch12-probabilities.md](../book/ch12-probabilities.md) |
| Ch 13 Hindsight | [ch13-hindsight.md](../book/ch13-hindsight.md) |
| Ch 14 Improving Analysis | [ch14-improving-analysis.md](../book/ch14-improving-analysis.md) |
| Full cleaned extract | [_source-cleaned.md](../book/_source-cleaned.md) |
