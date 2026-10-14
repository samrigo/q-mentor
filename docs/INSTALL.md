# Install, update, roll back, remove

## Option A — Copilot CLI plugin (Agent Plugins 1.0.0)

```bash
git clone -b Claude-v3 https://github.com/samrigo/q-mentor.git   # v3.1.1 lives on this branch
copilot plugin install ./q-mentor                                 # "Installed 17 skills"
copilot plugin list                                               # q-mentor (v3.1.1)
copilot skill list --json                                         # 17 q-mentor-* skills, source "plugin"
```

Observed with Copilot CLI 1.0.97 on 2026-10-14 (no login needed for these commands). Direct installs from a path
or repository print a deprecation notice; future CLI releases expect `plugin@marketplace` installs.

Inside a session: `/agent` should list **q-mentor**; ask "What can Q-Mentor do?" for the registry-derived menu.
Sixteen skills are user-invocable; `q-mentor-orchestrate` is internal.

- Update: `copilot plugin update q-mentor` (or reinstall from a newer checkout).
- Disable / enable: `copilot plugin disable q-mentor` / `enable` — disabled means zero q-mentor skills listed.
- Remove: `copilot plugin uninstall q-mentor`.
- Pin a release: check out a tag or commit SHA before installing; review the diff before upgrading.
  `copilot plugin install samrigo/q-mentor` would install the default branch (`main`), not this one.

## Option B — repository-local (cloud agent, Copilot app, IDE agent mode)

```bash
python scripts/deploy_repo_local.py --target /path/to/repo --dry-run
python scripts/deploy_repo_local.py --target /path/to/repo --targets qiskit dwave --hardware superconducting --domains finance
```

Copies skills to `.github/skills/`, the agent to `.github/agents/`, and the registries, schemas, templates, the help
renderer/routers/linter, and the selected knowledge packs to `.github/q-mentor/`. Writes
`.github/q-mentor/MANIFEST.json` (versions, SHA-256 per file). No symlinks.

- Update: re-run. Files you changed are reported as `CONFLICT` and nothing is written (`--force` replaces them).
  Updating from another version first saves the replaced files under `.github/q-mentor/backup/<old version>/`.
- Roll back: `--rollback` restores the most recent backup and its manifest.
- Remove: `--uninstall` deletes only unchanged files listed in the manifest (and the backup).
- Lifecycle test: `python scripts/test_deploy.py` (set `QMENTOR_COPILOT_BIN` to also check `copilot skill list`).

## Run the examples (optional)

Each example folder has its own lock (CPython 3.13, x86_64 Linux):

```bash
cd examples/bond-selection/cirq && uv venv && uv pip sync requirements.lock && python -m pytest -q
python scripts/validate_examples.py          # every folder, each in a fresh environment
```

## Limits

- Client checks marked `unverified` in `registry/compatibility.yml` need a licensed Copilot session.
- No MCP servers, hooks, web services, telemetry, or paid quantum jobs are included. Credential-gated scripts
  (`run_remote.py`) refuse to run without `QMENTOR_ALLOW_REMOTE=1` and an explicit approval.
