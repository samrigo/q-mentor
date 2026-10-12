# Cost, security, and governance

## Approval gates

Q-Mentor may teach, frame, generate local code, and run offline tests. It pauses for explicit approval before: remote provider execution, paid usage, credentials, production changes, cryptographic changes, organization-wide deployment, or non-public data. If your organization has not approved Copilot custom agents/plugins for the target data class, stop and route to AI-governance and security owners.

## Data boundaries

- Public or synthetic data by default; `ProblemSpec.provenance.data_class` must be `synthetic` or `public` (enforced in code and schema).
- No secrets, tokens, account numbers, client identifiers, positions, or proprietary models in prompts, fixtures, logs, lessons, or reports. CI runs a secret-pattern scan.
- Provider credentials stay in approved secret stores; no skill reads them.
- Generated code, investment models, and cryptographic recommendations require qualified human review.

## Threat model

| Risk | Control in this repository |
|---|---|
| Instructions hidden in documents or code | Agent rule 10; `behavior-prompt-injection` eval |
| Hallucinated SDK APIs | Version pins (`requirements-lock.txt`), imports exercised in CI, `behavior-version-drift` eval |
| Invalid cross-paradigm translation | `CapabilityReport` first; all-state equivalence; Pulser geometry gate; tamper test |
| False quantum claims | Evidence levels, verdict caps, `advantage_claimed` schema rule, advantage-claim evals |
| Cost runaway | Lazy skills, <=3 packs per skill, no default remote jobs |
| Data leakage | Synthetic defaults, sanitized lessons, no conversation retention |
| Supply chain | Minimal base deps, optional extras, dependency review on PRs |
| Unsafe crypto migration | Inventory only; NIST links; security-owner next step |
| Stale research | `last_verified` dates, candidate status, maintainer promotion |
| Self-improvement drift | Failing eval first, full regression, token comparison, human merge |

## Token and credit budget

- One skill per request; each `SKILL.md` <= 120 lines; each pack <= ~1,000 tokens (validated).
- Install only the domain and target packs a team uses (`deploy_repo_local.py --targets`).
- Browse only inside research/freshness tasks; otherwise rely on the pinned source registry.
- Organization pilots: small group, per-user hard limits, stop-at-limit budgets, separate hardware and AI-credit budgets. Measure credits per accepted result, tokens per skill, retry rate, eval pass rate, share of classical verdicts. Do not reward message volume. Check GitHub's current billing docs before setting policy; prices and models are not encoded here.

## Release gates

All fixed evals pass on supported clients; no high-severity dependency or secret finding; sources and versions re-checked; every coverage row has a skill, template/schema, eval, and stop condition; demo reproduces from a clean environment; limits visible in release notes; organizational approvals recorded outside this public repository.
