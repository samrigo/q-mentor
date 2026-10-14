---
id: improvement
contract: qmentor.response.v3
skills: [q-mentor-improve]
lead: Failure
fields: [Proposed change, Regression, Review]
optional: []
repeatable: false
cap_words: 160
machine: {Failure: result, Proposed change: evidence, Regression: validation, Review: next_action}
must_carry: [the sanitized lesson or changed source, the failing eval first, consent and human review]
---
# Template `improvement` — eval-first change proposal

```text
Failure: {sanitized failure, opted-in lesson, or changed primary source; consent record id}
Status: {status}
Proposed change: {smallest prompt/pack/code change and the failing eval added first}
Regression: {full-suite result and token-cost comparison, or "not run"}
Review: {human reviewer and PR plan; never auto-merge}
```
