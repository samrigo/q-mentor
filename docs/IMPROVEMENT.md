# Safe self-improvement

Q-Mentor does not retrain itself or silently remember chats. It improves through a governed repository loop:

```text
opted-in lesson, observed failure, or changed research
  -> sanitized candidate file               (templates/conversation-lesson.md, schemas/lesson-candidate.schema.json)
  -> failing eval added first               (evals/incidents/YYYY-MM-DD-slug.yml)
  -> smallest prompt / pack / code change
  -> full regression + token-cost comparison (python scripts/run_evals.py; captured responses)
  -> human-reviewed pull request
  -> versioned release + CHANGELOG entry
```

## Conversation lessons

- Asked at most once, at the end of a material workflow. Silence means no.
- The user sees and edits the candidate before any write.
- Contains: consent, prompt category, expected vs actual, risk, sanitized evidence, affected skill, client/model/version, counterexample, proposed assertion, scope (`personal`, `repository`, `plugin`), retention.
- Never contains: transcripts, source code, secrets, client or personal data. The schema rejects `contains_transcript: true` and missing consent.
- Personal preferences stay personal unless the user promotes them. Factual corrections need a source or reproducible test.
- Organization-specific lessons go to a separately approved **private** pack, never this public plugin.

## Research updates

1. `/q-mentor-research` produces a `candidate` evidence card.
2. A maintainer compares it with existing cards, records contradictions and replication status.
3. Add or update evals that the new knowledge should change.
4. Promote a compact claim into the relevant pack with `source`, `source_date`, `last_verified` in `knowledge/sources.yml`.
5. Keep negative and null results.

## Acceptance

A change is accepted only if the motivating eval passes, nothing regresses, and median eval tokens do not rise materially without written justification. `/q-mentor-improve` proposes; it never merges.
