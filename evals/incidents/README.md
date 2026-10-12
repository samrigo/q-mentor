# Incident and lesson evals

Each file here is created by `q-mentor-improve` **before** the fix it motivates, so it fails first.

- File name: `YYYY-MM-DD-<short-slug>.yml`, one eval case (schema: `schemas/eval-case.schema.json`, `suite: incidents`).
- Alongside it, a sanitized lesson candidate (`*.lesson.json`, schema: `schemas/lesson-candidate.schema.json`): explicit consent, no transcript, no code, no client or personal data.
- A fix is accepted only when this eval passes, the full suite does not regress, and median eval tokens do not rise without justification. A human merges.
