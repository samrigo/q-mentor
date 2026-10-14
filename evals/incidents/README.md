# Incidents and lesson candidates (eval-first improvement loop)

One YAML file per sanitized incident, named `NNN-short-slug.yml`, using the fields of
`templates/conversation-lesson.md` plus `origin` (`conversation` | `build-observation` | `research-update`).
`scripts/validate_incidents.py` enforces:

- a conversation-derived incident has an explicit consent record (silence means no);
- `proposed_assertion` points at an existing test or eval case (the failing eval comes first);
- no raw transcripts, source code blocks, credentials, e-mail addresses, or account-like numbers;
- scope is `personal`, `repository`, or `plugin`; personal lessons never enter this public plugin.

`000-example.yml` shows the format. `001`–`004` are real build observations from 3.1.1, each already backed by a
passing regression test.
