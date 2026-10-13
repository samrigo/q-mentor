# How Q-Mentor improves (and what it never does)

Q-Mentor does not retrain itself or remember chats. It improves through reviewed pull requests.

```text
opted-in lesson | failing eval | changed primary source
  -> sanitized candidate (templates/conversation-lesson.md or an EvidenceCard)
  -> failing eval added first (evals/incidents/ or the relevant eval folder)
  -> smallest prompt / pack / code change
  -> full regression + median-token comparison
  -> human-reviewed PR -> versioned release + CHANGELOG
```

## Conversation lessons
- At the end of a material workflow Q-Mentor may ask once whether to save a sanitized lesson. Silence means no.
- The user sees and edits the candidate before any file write. No transcripts, source code, client or personal data.
- Scope defaults to `personal`; `repository` or `plugin` only on explicit promotion.
- Factual corrections need a source or a reproducible test.

## Research updates
`q-mentor-research` creates `candidate` evidence cards. A maintainer compares them with existing
cards, records contradictions and replication, adds or updates evals, then promotes a compact
claim into a pack. Negative and null results are kept.

## Rejection rule
A candidate that fixes one case but harms routing, accuracy, privacy, format compliance or token
cost is rejected. Record the rollback commit in the PR.
