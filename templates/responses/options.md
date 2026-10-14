---
id: options
contract: qmentor.response.v3
skills: [q-mentor-brainstorm]
lead: Best option
fields: [Alternatives, Tradeoff, Next]
optional: []
repeatable: false
cap_words: 140
machine: {Best option: result, Alternatives: evidence, Tradeoff: uncertainty, Next: next_action}
must_carry: [a classical path, why a quantum path is or is not worth exploring, at most five candidates]
---
# Template `options` — brainstorm

```text
Best option: {the single best candidate and its readiness}
Status: {status}
Alternatives: {at most four more, each with readiness; at least one is classical}
Tradeoff: {the assumption or falsifier most likely to change the ranking; cost}
Next: {frame the chosen option, or the one missing input}
```

A larger ranked table (≤ 5 rows: option · paradigm · readiness · assumption · falsifier) may follow in
technical/detailed mode; it is outside the prose cap only when the user asked for detail.
