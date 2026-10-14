---
id: frame
contract: qmentor.response.v3
skills: [q-mentor-frame]
lead: Problem
fields: [Model, Assumption, Check]
optional: []
repeatable: false
cap_words: 140
machine: {Problem: result, Model: evidence, Assumption: uncertainty, Check: next_action}
must_carry: [objective, units and constraints, the unresolved assumption, a feasibility check]
---
# Template `frame` — problem framing

```text
Problem: {the decision in one sentence: variables, objective direction, success measure}
Status: {status}
Model: {objective with units, constraints and penalties; artifact path of the ProblemSpec/CanonicalProblem}
Assumption: {the one unresolved assumption that would change the model}
Check: {the feasibility or enumeration check run (or to run) and its observed result}
```

The full `ProblemSpec`/`CanonicalProblem` lives in an artifact validated by
`schemas/canonical-problem.schema.json`; the answer links it rather than repeating it.
