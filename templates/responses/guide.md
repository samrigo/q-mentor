---
id: guide
contract: qmentor.response.v3
skills: [q-mentor-help, q-mentor-learn]
lead: Answer
fields: [When to use, Next]
optional: []
repeatable: false
cap_words: 100
full_menu_cap_words: 350
machine: {Answer: result, When to use: evidence, Next: next_action}
must_carry: [one plain-language explanation or the best 1-3 skills, a prerequisite or tiny example]
---
# Template `guide` — help and learn

Use for `q-mentor-help` (skill menu, "which skill fits?") and `q-mentor-learn` (one concept).

```text
Answer: {one plain-language explanation, or the best 1-3 skills for the stated task}
Status: {complete | needs-input | blocked | unsupported | unverified}
When to use: {trigger, prerequisite, and output; or the analogy + one formula + common misconception}
Next: {one concrete action or the single missing input}
```

- `help` renders rows from `registry/skills.yml` only (`scripts/render_help.py`). On "all skills" it may add one
  table `skill | use when | prerequisite | output` (up to 20 rows / 350 words). Never a second hand-written menu.
- `learn` carries a domain analogy, one formula, one misconception, and one source id from `knowledge/sources.yml`.
- Business audience: no unexplained acronym. Technical audience: may link a pack or schema path.
- A help-only question stays read-only; an action request hands the chosen skill to the orchestrator.
