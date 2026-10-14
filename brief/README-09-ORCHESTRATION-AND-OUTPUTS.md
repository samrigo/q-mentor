# Orchestration and Response Contracts

V3 makes skill selection automatic, the help menu discoverable, and final answers task-shaped. The user states an outcome; Q-Mentor chooses the smallest safe skill chain and returns one compact result.

## Automatic skill orchestration

Create `registry/skills.yml` with one entry per skill:

```yaml
name: q-mentor-translate
intents: [convert, translate, port, compare targets]
requires: [CanonicalProblem, ProgramIR]
produces: [CapabilityReport, TranslationRecord]
prerequisites: [q-mentor-frame]
follow_ons: [q-mentor-convert, q-mentor-evaluate]
side_effects: none
template_id: mapping
```

The custom agent—not an assumed portable skill-calling API—owns orchestration:

1. Infer the requested outcome and select one primary skill.
2. Add only missing prerequisites; reuse valid existing artifacts.
3. Topologically sort the chain and reject cycles or duplicate execution.
4. Run skills sequentially, passing typed artifacts rather than copied prose.
5. Add a follow-on only when it is required to finish the user's stated task.
6. Stop for approval only before paid, credentialed, remote, destructive, production, cryptographic, or non-public-data actions.
7. Stop for input only when a missing choice materially changes the result.
8. Cap a turn at five skills. For longer workflows, write a checkpoint artifact and resume with a fresh context.

The custom-agent prompt consults the registry at the start of every task. The `q-mentor-orchestrate` skill sets `user-invocable: false` and `disable-model-invocation: false`; its description names multi-phase, conversion, implementation, and validation triggers. Every other `SKILL.md` resolves `registry/skills.yml` from the plugin root or `.github/q-mentor/registry/skills.yml` in repository mode, then consults it when required input is absent or its result needs validation. A missing or invalid registry returns `blocked`; the skill does not guess. Users never need to know skill names. If the Copilot surface cannot dynamically load another skill, the orchestrator reads the named `SKILL.md`; it must not pretend that a slash command executed.

`q-mentor-help` is user-invocable and automatically triggered by questions such as “what can you do?”, “which skill?”, or “how do I use Q-Mentor?”. It lists the live registry's skill names, one-line jobs, trigger examples, prerequisites, and output template. It can filter to a task (“help with converting Pulser to Classiq”) and then hand off to the chosen skill when the user requests action. Test that every registered skill appears exactly once and that a new skill appears without editing the help prompt.

Build its `SKILL.md` from this minimal contract: `name: q-mentor-help`; description: “Use when the user asks what Q-Mentor can do, which skill fits a task, or how to start”; `user-invocable: true`; `disable-model-invocation: false`; no shell, write, or network preapproval. Read only `registry/skills.yml`. By default show the best one to three skills with when-to-use, input/prerequisite, and output; on “all skills,” render every registry entry in the compact [guide template](README-13-RESPONSE-TEMPLATES.md). Never invent a skill, maintain a second menu, or make a user type a slash command to continue an authorized task. A help-only question stays read-only; an action request hands the selected skill to the orchestrator.

## Required handoffs

The table omits the `q-mentor-` prefix for brevity.

| Skill completes | Automatically consider |
|---|---|
| `learn` | `research` for a current claim; `frame` for a real problem |
| `research` | `evaluate` before promoting a claim |
| `brainstorm` | `frame` and `verdict` for a selected option |
| `frame` | `verdict`; then `design` only when justified |
| `verdict` | `design` for an approved experiment or `exec` for a decision-only request |
| `design` | `translate` for named targets; then `evaluate` |
| `translate` | `convert` when code is requested; otherwise `evaluate` |
| `convert` | `test`, then `review` for material code; `evaluate` if the optimization claim needs assessment |
| `evaluate` | return to `design` on failure; otherwise `implement` or `exec` |
| `implement` | always `test`; then `review` for material code |
| `test` | `implement` for a scoped repair, `review` on pass, `exec` for results |
| `review` | `implement`/`test` for accepted fixes; `pqc-scan` when cryptography is in scope |
| `pqc-scan` | `review` and a human security owner; never automatic migration |
| `exec` | `improve` only after explicit opt-in |
| `improve` | `research` or `test`, then a human-reviewed change proposal |
| `help` | the skill the user chooses, only when the user asks to run it |

This table describes possible edges, not a command to run every skill. The registry and requested outcome determine the minimal path.

## Mandatory answer contract

Use `qmentor.response.v3` and the template routing, copy-ready shapes, word budgets, and JSON schema in [README-13](README-13-RESPONSE-TEMPLATES.md). `registry/skills.yml` holds each skill's `template_id`; the corresponding `SKILL.md` must cite it and include the mandatory per-answer instruction. The agent validates **every** user-facing answer—including clarification, failure, unsupported, and direct skill invocation—against the selected template. Multi-skill chains produce one final answer from the terminal skill's template, not a report from each skill.

A failure names the first actionable broken gate and one repair. A code answer contains complete files or a scoped diff plus observed checks. A sketch is `draft`, never a completed conversion. An explicit user format or depth instruction overrides headings while preserving material uncertainty and validation facts.

Test default, business, technical, failure, direct invocation, automatic handoff, and machine mode on a strong and an economical supported Copilot configuration. Assert exact template selection, required facts, stable heading order, word budget, valid citations, JSON schema, no duplicate conclusion, and no loss of uncertainty. Track median output tokens and retries; reject a prompt change that becomes short by omitting evidence.
