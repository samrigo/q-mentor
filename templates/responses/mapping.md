---
id: mapping
contract: qmentor.response.v3
skills: [q-mentor-translate]
lead: Route
fields: [Preserved, Lost / limited, Next]
optional: []
repeatable: false
cap_words: 160
machine: {Route: result, Preserved: evidence, Lost / limited: uncertainty, Next: next_action}
must_carry: [source and target computing model, capability class spelled out, semantic loss or none]
---
# Template `mapping` — translate

```text
Route: {source model -> target model; exact | conditional | reimplementation | approximate | unsupported}
Status: {status}
Preserved: {objective/operator, bit order, measurement, decode that survive; proof fixture}
Lost / limited: {dropped or changed semantics (pulses, geometry, postselection, noise) or "none"}
Next: {convert with tests, choose another target, or the one missing input}
```

Spell out the class word; the letters E/C/R/A/U may follow in brackets for technical readers.
