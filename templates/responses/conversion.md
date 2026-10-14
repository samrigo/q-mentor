---
id: conversion
contract: qmentor.response.v3
skills: [q-mentor-convert]
lead: Result
fields: [Route, Equivalence, Optimization, Validation, Files]
optional: [Optimization]
repeatable: false
cap_words: 180
machine: {Result: result, Route: evidence, Equivalence: evidence, Optimization: evidence, Validation: validation, Files: artifacts}
must_carry: [complete target artifacts or exact diff, the route class spelled out, observed tests]
---
# Template `conversion` — cross-hardware conversion

```text
Result: {what was produced, or why no executable conversion is valid}
Status: {status}
Route: {source model -> target model; exact | conditional | reimplementation | approximate | unsupported}
Equivalence: {what was preserved, what was not, and the toy proof/decoder}
Optimization: {declared metric, fixed budget, result or "not improved"}   <- only for optimization requests
Validation: {syntax, import, local run, semantic test, versions; observed vs unavailable}
Files: {complete target files/diff and test fixture, or none}
```

Show this compact block before inline code. Never truncate code to fit the cap; code blocks are outside it.
"Runnable" needs imports, pins, entry point, test command, and a clean-environment observation; otherwise label
the artifact `illustrative` or `unverified`. `optimized` is allowed only with an `OptimizationRecord`
(`schemas/optimization-record.schema.json`) whose status is `improved`.
