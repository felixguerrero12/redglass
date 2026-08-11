# Source — checklist router + line slices

**File:** `~/psychology-of-intelligence.md` (about 1448 lines)

Richards J. Heuer, Jr., *Psychology of Intelligence Analysis* (CSI/CIA, 1999).

This skill teaches method. It does not put the full book into the prompt.

## How to read

Never load the entire file.

```text
Read path=~/psychology-of-intelligence.md offset=<start> limit=<end-start+1>
```

Or:

```bash
sed -n '<start>,<end>p' ~/psychology-of-intelligence.md
```

1. Walk the agent checklist in [../SKILL.md](../SKILL.md).
2. If you need Heuer text, open only that step line range.
3. Usual max: one step slice. Rarely two short slices.
4. Do not `cat` the full book.

## Agent → lines

| Agent | Lines |
|---|---:|
| problem-framer | 1362–1377; 779–836 |
| hypothesis-generator | 434–569; 837–860 |
| collector | 570–656; 1383–1387 |
| evaluator | 837–949 |
| selector-reporter | 900–920; 1397–1402 |
| monitor | 920–926; 1403–1406 |
| bias-guard | 970–1050 |
| open-mind | 283–361; 657–778 |
| learner-postmortem | 1285–1361 |

Full checklist text also sits in Ch. 14 (1362–1448).

## Appendix: chapter catalog

| Section | Lines |
|--------:|------:|
| Front matter / TOC | 1–77 |
| Author’s Preface | 78–85 |
| Foreword (MacEachin) | 86–104 |
| Introduction (Davis) | 105–250 |
| Ch 1 Thinking | 251–282 |
| Ch 2 Perception | 283–361 |
| Ch 3 Memory | 362–433 |
| Ch 4 Strategies | 434–569 |
| Ch 5 More Info? | 570–656 |
| Ch 6 Open Mind | 657–778 |
| Ch 7 Structuring | 779–836 |
| Ch 8 ACH | 837–949 |
| Ch 9 Cognitive Biases | 950–969 |
| Ch 10 Evidence biases | 970–1050 |
| Ch 11 Cause and Effect | 1051–1192 |
| Ch 12 Probabilities | 1193–1284 |
| Ch 13 Hindsight | 1285–1361 |
| Ch 14 Improving Analysis | 1362–1448 |
