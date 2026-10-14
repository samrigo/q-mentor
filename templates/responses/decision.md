---
id: decision
contract: qmentor.response.v3
skills: [q-mentor-verdict, q-mentor-exec]
lead: Decision
fields: [Why, Cost / risk, Next gate]
optional: []
repeatable: false
cap_words: 140
machine: {Decision: result, Why: evidence, Cost / risk: uncertainty, Next gate: next_action}
must_carry: [a named classical baseline, confidence, the business implication, the decision boundary]
---
# Template `decision` — verdict and executive brief

```text
Decision: {classical now | research or teaching PoC only | run a bounded quantum experiment | candidate experiment | no-go, and why}
Status: {status}
Why: {one measured fact against a named classical baseline; readiness score and hard gates; confidence}
Cost / risk: {time, money, or technical risk most likely to change the choice}
Next gate: {one measurable threshold, approval, or material question}
```

`exec` builds only from `ResultRecord`s or a `Verdict`; without them it returns `Status: blocked`.
"Classical now" is a first-class decision; never soften it because the user asked for quantum.
