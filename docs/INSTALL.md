# Install, update, remove

## Option A — Copilot CLI plugin (Agent Plugins 1.0.0)

```bash
git clone -b Claude-v2 https://github.com/samrigo/q-mentor.git   # v2 lives on this branch
copilot plugin install ./q-mentor                                 # install from the clone
copilot plugin list                                    # confirm "q-mentor" is installed
```

Inside a session: `/agent` should list **q-mentor**; `/skills list` should list the 14
user-invocable `q-mentor-*` skills (`q-mentor-orchestrate` is internal). For scripted checks,
`copilot skill list --json` where your CLI version provides it.

Pin a release for reproducibility: check out a tag or commit SHA before installing and review the diff before upgrading. `copilot plugin install samrigo/q-mentor` installs the default branch (`main`), not this one.

- Update: `copilot plugin update q-mentor`
- Remove: `copilot plugin uninstall q-mentor` (uses the manifest `name`, not the folder)
- Installed components are cached; reinstall after local edits.

If an earlier plugin named `q-mentor` is installed, uninstall it first — this v2 package uses the same name.

## Option B — repository-local (cloud agent, Copilot app, IDE agent mode)

```bash
python scripts/deploy_repo_local.py --target /path/to/your/repo --dry-run
python scripts/deploy_repo_local.py --target /path/to/your/repo --targets qiskit dwave --domains finance
```

This copies skills to `.github/skills/`, the agent to `.github/agents/`, and the registry,
schemas, templates and selected knowledge packs to `.github/q-mentor/`. It refuses to
overwrite files you changed since the last deployment and writes
`.github/q-mentor/MANIFEST.json` with versions and SHA-256 checksums. No symlinks.

- Update: re-run the script; changed files are reported, not overwritten (`--force` to replace).
- Remove: `python scripts/deploy_repo_local.py --target /path --uninstall` removes only files listed in the manifest whose checksum is unchanged.

## Optional: run the examples

Each example folder has its own lock. Example:

```bash
cd examples/bond-selection/dwave
uv venv && uv pip sync requirements.lock && python -m pytest -q
```

## Limits

- Supported clients are listed in `registry/compatibility.yml`; client checks marked `unverified` have not been run against a live Copilot session yet.
- Locks target CPython 3.13 on x86_64 Linux.
- No MCP servers, hooks, web services, telemetry or paid quantum jobs are included.
