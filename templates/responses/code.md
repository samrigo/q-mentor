---
id: code
contract: qmentor.response.v3
skills: [q-mentor-implement, q-mentor-test]
lead: Result
fields: [Files, Checks, Next]
optional: []
repeatable: false
cap_words: 180
machine: {Result: result, Files: artifacts, Checks: validation, Next: next_action}
must_carry: [complete files/diff or test report, exact commands, pass/fail counts]
---
# Template `code` — implement and test

```text
Result: {what changed or which test passed/failed}
Status: {status}
Files: {paths to complete files/diff or test report; "none" if blocked before writing}
Checks: {exact command and observed result; include failing test name and cause}
Next: {one repair, review, or no action}
```

Report only the highest observed validation state: draft, syntax-checked, imported, locally-executed,
target-validated. A credential-gated step is `unverified`, never `passed`. Complete files follow the block.
