---
id: review
contract: qmentor.response.v3
skills: [q-mentor-review]
lead: Finding
fields: [Impact, Evidence, Fix / owner]
optional: []
repeatable: true
max_repeats: 3
cap_words: 140
machine: {Finding: result, Impact: uncertainty, Evidence: evidence, Fix / owner: next_action}
must_carry: [the highest-severity actionable finding first, or "No findings" with the review scope]
---
# Template `review` — findings only

```text
Finding: {[severity] highest-severity actionable finding, or "No findings" + scope reviewed}
Status: {status}
Impact: {what goes wrong, for whom}
Evidence: {file:line, failing check, or source}
Fix / owner: {smallest fix and who decides}
```

Repeat the `Finding … Fix / owner` block at most three times (Status appears once); link a findings artifact
for more. No patch unless the user asked for a fix.
