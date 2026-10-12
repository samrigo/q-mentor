# Cost, Security, and Governance

## Cost objective

Minimize total attempts and total context, not just the length of one prompt. A slightly clearer prompt and a deterministic test are cheaper than repeated agent correction.

## Construction budget

- Use a strong reasoning model once for architecture and hard math; use Auto or a lighter model for scoped implementation, tests, and documentation.
- Start a fresh session for each milestone. Do not carry research history into implementation.
- Give Copilot the target tree, exact test command, relevant files, and stopping condition up front.
- Keep changes small enough to review and revert. Reject unrelated refactors.
- Run deterministic checks before asking a model to diagnose anything.
- Set an AI-credit session limit where the client supports it.
- Do not use parallel subagents for this small MVP unless a measured build step benefits from them.

## End-user token budget

- Load one skill per request; never inject all provider and math packs.
- Install only the domain and execution-target packs a team uses; keep Pasqal, PennyLane, and other SDK dependencies optional.
- Keep each `SKILL.md` under roughly 120 lines and each knowledge pack under roughly 1,000 tokens.
- Cap defaults using the product table in README-01; users can ask for depth.
- Prefer structured templates to repeated explanations.
- Use local code for enumeration, schema checks, matrix algebra, and report metrics.
- Use browsing only inside a research/freshness task; normal learning and implementation should rely on the pinned source registry.
- Start a new chat when the problem changes; compact long CLI sessions.
- Avoid a large MCP tool catalog. The MVP needs no MCP tools.
- Store no raw chat corpus. An opted-in lesson is a short structured summary and one eval candidate, which is cheaper and safer to review.
- Preserve model cache by choosing model/reasoning/tool settings before the session and avoiding mid-session churn.

GitHub pricing and model availability change. As checked on `2026-10-11`, GitHub documents token-based AI Credits, model-dependent rates, an Auto-selection discount on paid plans, usage dashboards, session limits, and administrator budget controls. Verify the current official pages before setting financial policy; do not encode prices or model names into the plugin.

## Budget controls

For an organization deployment:

1. Assign a small pilot group.
2. Set a universal per-user hard limit before launch.
3. Set cost-center or organization overage budgets and enable stop-at-limit.
4. Keep paid hardware and AI-credit budgets separate.
5. Review usage by skill, accepted outcome, retries, and model class—not raw prompt content.
6. Expand only after the pilot meets quality and cost thresholds.

Useful metrics: AI credits per accepted result, tokens per skill, retry rate, eval pass rate, percentage of classical verdicts, provider-job spend, and time to reviewed code. Do not reward message volume.

## Data and action boundaries

- Public or synthetic data only by default.
- Never place secrets, tokens, account numbers, client identifiers, positions, or proprietary models in prompts, fixtures, logs, incidents, or generated reports.
- Repository access does not imply permission to use every file as model context. Respect content exclusions and least privilege.
- Provider credentials stay in approved secret stores and are never read by documentation skills.
- Remote execution requires a visible provider, backend, estimated cost, data classification, and explicit confirmation.
- Generated code, investment models, and cryptographic recommendations require qualified human review.

## Threat model

| Risk | Control |
|---|---|
| Instructions hidden in documents or code | Treat retrieved content as data; follow trusted plugin and repository instructions only |
| Hallucinated SDK APIs | Pin versions, cite official docs, compile/import in CI |
| Invalid cross-paradigm translation | Capability report, exact/approximate/unsupported status, energy and hardware-constraint tests |
| False quantum claims | Evidence levels, classical baseline, advantage-claim evals |
| Cost runaway | Lazy skills, session limits, org budgets, no default remote jobs |
| Data leakage | Synthetic defaults, content exclusions, sanitization, no conversation retention |
| Supply-chain compromise | Lockfiles, dependency review, provenance, minimal dependencies |
| Unsafe crypto migration | Inventory only; NIST sources; security-owner approval |
| Stale or overstated research | Evidence cards, freshness dates, contradictions, replication status, maintainer promotion |
| Conversation privacy or preference leakage | Explicit opt-in, user-visible sanitization, scoped lessons, no transcripts or cross-user promotion by default |
| Self-improvement drift | Failing eval first, full regression, token-cost comparison, human merge, signed release |

## Approval gates

The plugin may teach, frame, generate local code, and run offline tests. It must pause for explicit approval before remote provider execution, paid usage, credentials, production changes, cryptographic changes, organization-wide deployment, or use of non-public data.

If the organization has not approved GitHub Copilot custom agents/plugins for the target data class, stop and route the user to the AI governance and security owners.

