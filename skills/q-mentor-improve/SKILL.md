---
name: q-mentor-improve
description: >
  Turn a recorded failure, approved conversation lesson, or changed primary source
  into an eval-first change proposal. Use only after explicit user opt-in.
---

# q-mentor-improve

## Safe self-improvement loop

```
opted-in conversation lesson, observed failure, or changed research
  → sanitized candidate file
  → failing eval added first
  → smallest prompt/pack/code change
  → full regression and cost comparison
  → human-reviewed pull request
  → versioned release and changelog
```

## Preconditions

- Explicit user consent for any conversation-derived lesson.
- User sees and edits the candidate before any file write.
- Silence means no.

## Lesson candidate fields

- Explicit consent
- Prompt category
- Expected vs actual
- Risk
- Sanitized evidence
- Affected skill
- Model / client / version
- Counterexample
- Proposed assertion
- Scope (personal / repository / plugin)
- Retention decision

Never retain raw transcripts, source code, or unauthorized data.

## Knowledge links

- `templates/conversation-lesson.md`
- `evals/`
