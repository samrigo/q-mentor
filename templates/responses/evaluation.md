---
id: evaluation
contract: qmentor.response.v3
skills: [q-mentor-evaluate]
lead: Result
fields: [Baseline, Fairness / uncertainty, Next]
optional: []
repeatable: false
cap_words: 160
machine: {Result: result, Baseline: evidence, Fairness / uncertainty: uncertainty, Next: next_action}
must_carry: [same instance and budget, the metric, variability, the limit on the conclusion]
---
# Template `evaluation` — grade a paper, proposal, or experiment

```text
Result: {winner, tie, or insufficient evidence on the declared metric; scorecard total}
Status: {status}
Baseline: {classical or incumbent method, instance, metric, value}
Fairness / uncertainty: {same budget/seeds/instance? interval or limitation; evidence level 1-5}
Next: {one validation gate or decision}
```

Never compare a CVaR objective with mean energy as the same metric. The scorecard artifact follows
`templates/experiment-record.md`.
