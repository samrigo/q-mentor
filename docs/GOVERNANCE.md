# Cost, security and governance

## Approval gates
Q-Mentor may teach, frame, generate local code and run offline tests. It pauses for explicit
approval before remote provider execution, paid usage, credentials, production changes,
cryptographic changes, organisation-wide deployment, or non-public data. Remote example paths
require `QMENTOR_ALLOW_REMOTE=1` **and** `QMENTOR_CONFIRM_COST=yes`.

If your organisation has not approved GitHub Copilot custom agents/plugins for the data class
involved, stop and contact your AI governance and security owners.

## Data
Synthetic or public data only by default. Never put secrets, tokens, account numbers, client
identifiers, positions or proprietary models in prompts, fixtures, logs, incidents or reports.
Repository access does not imply permission to use every file as model context.

## Tool permissions
The agent declares `read, search, edit, execute, web` explicitly (never `*`). Skills pre-approve
only read/search (plus `web` for research and `edit` for implement/test/improve). No skill
pre-approves `shell`/`bash`/`execute`: every command is confirmed by the user.
Tool names in `allowed-tools` follow the Copilot custom-agent aliases; clients ignore names they
do not recognise, so nothing is pre-approved by accident.

## Token and AI-credit budget
- One skill at a time; at most five per turn; checkpoint longer workflows.
- Brief answers by default (≤ 180 words); detailed or machine mode on request.
- Each `SKILL.md` < 120 lines; each knowledge pack < ~1,000 tokens.
- Browsing only inside research/freshness tasks.
- Install only the domain and target packs you use (`deploy_repo_local.py --targets ... --domains ...`).
- Set per-user session limits and organisation budgets with stop-at-limit before a pilot; keep
  paid-hardware budgets separate from AI-credit budgets. Measure AI credits per accepted result,
  tokens per skill, retry rate, eval pass rate, share of classical verdicts.

Pricing and model availability change: use GitHub's official pages, not this file, as the source
of truth (`copilot-models-pricing`, `copilot-budgets`, `copilot-optimize-usage` in `knowledge/sources.yml`).

## Threat model (summary)
| Risk | Control in this repo |
|---|---|
| Instructions hidden in documents/code | Shared rule 12; `prompt-injection-in-document` eval |
| Hallucinated or stale SDK APIs | Pinned locks; `stale_apis` deny-list; clean-env import/run gate |
| Partial plausible code | Placeholder and undefined-name scan; validation states |
| Invalid cross-paradigm translation | CapabilityReport; Pulser refusal; energy-equivalence tests |
| Routing loops | Registry DAG check; duplicate/cycle routing evals |
| False quantum claims | Evidence levels; advantage linter rule; behaviour evals |
| Data leakage / conversation retention | Synthetic defaults; opt-in sanitized lessons only |
| Supply chain | Exact-pin locks; pinned GitHub Actions by SHA; dependency review in CI |
| Unsafe crypto migration | Inventory-only PQC skill; security-owner handoff |
