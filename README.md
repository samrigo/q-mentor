# Q-Mentor

**Honest, vendor-neutral quantum-computing guide for GitHub Copilot.**

Q-Mentor teaches concepts, researches evidence, screens problems, designs and implements experiments, tests results, and always names the strongest classical alternative. Finance is the first domain pack and reference demo—not a limit on the core architecture.

Brief version: `1.0.0` · Agent Plugins 1.0

## Install

### As an Agent Plugins 1.0 package

1. Clone or download this repository.
2. Install the plugin through your Copilot client’s plugin/marketplace flow, pointing at the repository root (the directory that contains `plugin.json`).
3. The custom agent `q-mentor` and all skills under `skills/` become available.

### Repository-local skills (IDE agent modes)

```bash
python scripts/deploy_repo_local.py
# copies skills into ./.github/skills/
```

### Remove

Uninstall the plugin from your client, or delete the `.github/skills/` copies.

## Skills (slash-style)

| Skill | Job |
|-------|-----|
| `q-mentor-learn` | Explain one concept |
| `q-mentor-research` | Evidence card from sources |
| `q-mentor-brainstorm` | ≤5 ranked use cases |
| `q-mentor-frame` | Business problem → math |
| `q-mentor-verdict` | Classical / PoC / experiment decision |
| `q-mentor-design` | Target-neutral design |
| `q-mentor-translate` | Map to two execution targets |
| `q-mentor-evaluate` | Scorecard for paper/proposal/experiment |
| `q-mentor-implement` | Smallest approved code change |
| `q-mentor-test` | Deterministic & cross-provider tests |
| `q-mentor-review` | Math, code, claims, alternatives |
| `q-mentor-pqc-scan` | Crypto inventory |
| `q-mentor-exec` | One-page leadership brief |
| `q-mentor-improve` | Eval-first improvement proposal |

## Lifecycle

```
learn/research → brainstorm → frame → verdict → design → translate
              → evaluate → implement → test/review → exec → improve
```

## Demo: six-bond selection

Synthetic didactic problem. Exact classical optimum is unique:

```
x* = [1, 0, 1, 0, 1, 0]   # bonds A, C, E
energy = -9.3725
```

Expected verdict: **classical now; quantum teaching PoC only**.

```bash
python scripts/validate_math.py
```

## Safety & governance

- Never claims quantum advantage without reproducible end-to-end evidence.
- Always names a classical baseline.
- No paid quantum jobs or credentials without explicit approval.
- Public / synthetic data by default.
- Self-improvement is opt-in, sanitized, eval-first, human-reviewed PRs—not silent memory.

## Validation

```bash
python scripts/validate_package.py
python scripts/validate_math.py
```

## License

MIT
