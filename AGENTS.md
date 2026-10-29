# AGENTS.md

Persistent instructions for any AI agent working in this repository, whatever LLM or tool it runs on. Read this file fully before changing anything.

## What this project is

CraftApps — *Craft your own apps.* A collection of portable AI agent skills that guide a person from discovering a problem in their own life to building, verifying, and (optionally) sharing a small piece of software they own.

It is a repository of skills and documentation. It is **not** an application, hosted service, framework, or orchestration engine.

**What gets made:** native apps (and, when enough, native automations such as scripts or Shortcuts) for the platforms the user already uses — iOS, macOS, Android, Windows, Linux, and so on. Not websites or hosted web services. The platform is chosen from the user's own devices, never assumed. Grown apps use the platform's built-in frameworks; every third-party library, SDK, backend, account, or cross-platform framework needs a stated reason. The same rule applies to this repository itself.

## Philosophy (applies to every change)

- **Security and privacy first — above every other goal.** Never read a user's private conversations directly; never send user data to anyone. When security conflicts with convenience, features, or speed, security wins.
- **Own your software.** Users control their applications, source code, and data.
- **Small is beautiful.** Prefer the smallest thing that solves the problem. A shortcut or script beats an app when it is enough.
- **Build for yourself first.** Software used by one person is still valuable.
- **Accessible to everyone.** Skills must work for people who have never written code.
- **Open and extensible.** Skills are plain, readable, customizable text.
- **Human agency.** AI proposes; the user decides. No consequential action without explicit approval.

## Current scope

Implemented: `discover-app`, `build-app` (v0), `share-app`, and `curate-app` (for the library maintainer). See `docs/ROADMAP.md`.

- Every skill adapts to the user's experience level; follow `skills/build-app/references/experience-levels.md` as the shared guide.
- Do not build a web app, backend, database, hosted service, multi-agent framework, or publishing automation.

## Repository map

```
AGENTS.md                 This file (agent instructions)
CLAUDE.md                 One-line pointer to AGENTS.md for tools that only read their own file
README.md                 Human-facing introduction
.claude-plugin/           Claude Code plugin and marketplace manifests
.codex-plugin/            Codex plugin manifest
.agents/plugins/          Codex marketplace manifest
docs/VISION.md            Why the project exists
docs/ARCHITECTURE.md      Skill contract, handoff artifacts, planned modules
docs/ROADMAP.md           Milestones and status
skills/<skill-name>/      One directory per skill (Agent Skills format)
  SKILL.md                Entry point: frontmatter + core instructions
  references/             Detail loaded on demand (templates, formats, rules)
  examples/               Small synthetic examples that ship with the skill
examples/                 Synthetic test fixtures with expected findings
  scripts/                Local helper scripts (stdlib only, no network)
scripts/validate-skills.sh  Structural checks for every skill
scripts/test_*.py         Tests for skill scripts
```

## Creating or modifying skills

Skills follow the open Agent Skills format (`SKILL.md` with YAML frontmatter; see https://agentskills.io/specification).

Rules:

1. **Directory name = `name` field.** Lowercase letters, digits, hyphens. CraftApps skills are named `<verb>-app` (for example `discover-app`, `build-app`): what the person wants to do, in their words. Inside a plugin they are also namespaced (`craftapps:build-app`).
2. **Frontmatter** contains `name` and `description`. The description says *when* to use the skill (triggers, user phrases, situations) in the third person — not a summary of its steps. Keep it under ~500 characters.
3. **Keep `SKILL.md` focused** (well under 500 lines). Move templates, format details, and long rules into `references/` and link to them by relative path from `SKILL.md`.
4. **Stay LLM-neutral and portable.** Skills must work with any capable LLM, cloud or local, and never require a specific AI provider, model, or agent product. Describe actions in plain language ("read the file", "ask the user"). Do not depend on tool names, slash commands, or features unique to one agent product in the core instructions. If agent-specific notes are unavoidable, isolate them in a clearly labeled section.
5. **Define the contract.** Every skill states its purpose, when to use it, inputs, outputs, boundaries, and how it hands off — following the skill contract in `docs/ARCHITECTURE.md`.
6. **Respect the handoff format.** Skills exchange Markdown files with YAML frontmatter (`craftapps_artifact`, `schema_version`, ...). Changing an artifact's structure means bumping `schema_version` and updating `docs/ARCHITECTURE.md`, the template in `references/`, and the examples in the same change.
7. **Examples are synthetic.** Never derive an example from real user data, even if anonymized.
8. **One skill at a time.** Finish, validate, and test a skill before starting the next.

## Security and privacy requirements (highest priority, non-negotiable)

- **Raw conversations never reach the AI.** Conversation exports and AI tool session logs are processed only by a local script with no AI and no network (`skills/discover-app/scripts/prepare_input.py`). The user reviews and approves the cleaned result before any agent reads it. Agents must not open raw exports or session logs in any way, even to inspect their format.
- **Never send user data to others**: no uploads, no third-party services, no telemetry, no sharing between users.

- **Never commit real personal data**: conversation exports, chat logs, notes, screenshots, generated reports about a real person, credentials, API keys, tokens, or signing material. `.gitignore` is a safety net, not permission.
- **Synthetic data only** in `examples/`, `skills/*/examples/`, docs, and tests. Mark synthetic files as synthetic.
- **Skills operate on explicitly provided input only.** A skill must never search the user's disk, browser, accounts, or apps for data on its own initiative. It reads the paths the user gives it.
- **Local by default.** Skills must not send user data to network services, APIs, or the web. If a future skill genuinely needs a network call, it must say exactly what is sent, where, and ask first.
- **Be honest about processing.** Skills that read personal material must tell the user that a cloud-hosted model sends what it reads to its provider, before reading it.
- **Pass only artifacts between skills.** A downstream skill reads the handoff artifact, never the user's raw inputs. The user approves artifacts at the checkpoints in `docs/ARCHITECTURE.md`.
- **Minimize and redact.** Outputs quote only what is needed as evidence and redact third-party personal details and secrets.
- **Generated personal outputs stay out of git.** Default output locations (such as `craftapps/`) are ignored in this repository, and skills that write `craftapps/` inside a person's own repository make it ignored there first.

## Quality expectations

- Write instructions that are specific, testable, and unambiguous. Prefer checklists and templates over vague advice.
- Scripts are allowed only when they serve a clear purpose that plain instructions cannot. Use POSIX `sh` or the Python 3 standard library; no package managers, no third-party packages, no network access. Keep each script small, commented, and runnable from the repo root.
- No dependencies, build systems, CI services, package manifests, or frameworks without explicit approval.

## Documentation requirements

Update documentation in the same change as the behavior it describes:

- `README.md` — the "What works today" status if capabilities change.
- `docs/ROADMAP.md` — milestone status.
- `docs/ARCHITECTURE.md` — skill contract, artifacts, or module list changes.
- The skill's own `SKILL.md`, references, and examples.

Write for a mixed audience: developers and people who do not code. Define jargon on first use.

## Testing expectations

Run before finishing any change to skills:

```sh
sh scripts/validate-skills.sh
python3 -I scripts/test_prepare_input.py
```

Behavioral testing for a skill:

1. In a fresh agent session, run the skill against a fixture in `examples/` (e.g. `examples/discovery/synthetic-ios-developer/input/`).
2. Compare the output with that fixture's `expected-findings.md` rubric.
3. Report the result honestly: which rubric items passed, which failed, and what was not tested.

Never claim a skill "works" or a change is "tested" without having run these checks. State what was verified and what was not.

## Process skills for contributors (optional)

If your agent has general process skills installed (for example [Superpowers](https://github.com/obra/superpowers)), use them for work on this repository:

- New skill or architecture change → `brainstorming` first, then ask for approval as above.
- Creating or editing any skill → `writing-skills`: run a baseline scenario without the change, then with it, and record both in the fixture's `evaluations.md`.
- Before saying a change is finished → `verification-before-completion`: run the checks in *Testing expectations* and read their output.

Inside the skills themselves, process skills are optional and conditional: each skill says which ones fit in a clearly labeled "Process skills (optional)" section, and CraftApps' rules take precedence. Never make a skill depend on them.

## Keep it simple and modular

- Each skill is independently useful. A user may invoke any stage directly with their own input.
- Skills communicate through files, not shared code or a runtime.
- Do not add orchestration until a real, repeated need is demonstrated and approved.
- Remove before you add. If a section, file, or option is not needed, delete it.

## Ask for approval before

- Changing the architecture, the skill contract, or the handoff artifact format.
- Adding a new skill, a new top-level directory, or a script.
- Adding any dependency, tool, CI, or infrastructure.
- Changing the license, or adding paid or differently-licensed content. Everything in this repository is MIT and free; never add payment code or license checks.
- Creating repositories, pushing, publishing, or any action visible outside this machine.

## Git conventions

- Small, focused commits with imperative subject lines (`Add discovery report template`).
- Review `git status` and the staged diff before every commit to confirm no personal data, exports, or secrets are included.
