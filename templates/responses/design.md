---
id: design
contract: qmentor.response.v3
skills: [q-mentor-design]
lead: Design
fields: [Why, Check, Next]
optional: []
repeatable: false
cap_words: 160
machine: {Design: result, Why: evidence, Check: validation, Next: next_action}
must_carry: [the architecture choice, a rejected alternative, an acceptance test]
---
# Template `design` — experiment and implementation design

```text
Design: {target-neutral architecture: canonical model, classical baseline, target plans (family · model · SDK · backend · support level)}
Status: {status}
Why: {why this design; the rejected alternative and why}
Check: {acceptance tests: energy equivalence, decode, seeds, budget, stop condition}
Next: {the first implementation or approval step}
```
