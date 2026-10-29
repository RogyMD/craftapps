# Architecture

CraftApps is a set of independent **agent skills** that pass work to each other as **plain files**. There is no runtime, server, framework, or orchestrator. The user's AI agent — any capable LLM, cloud or local, in any agent that can read files and run commands — is the runtime.

## Key decisions

| Decision | Choice | Why |
|---|---|---|
| What gets built | Native apps (or native automations) for the user's own platforms; not websites or hosted services | Local data, offline use, device capabilities, no server or account. |
| Platform choice | Taken from the user's devices; decided in the build plan | Build for what the person actually uses; never assume one platform. |
| Dependencies in crafted apps | Platform frameworks by default; each third-party library, SDK, backend, or account justified in writing | Less to break, update, and trust; apps keep working for years. |
| AI provider | None required — any capable LLM, cloud or local | No lock-in; a local model keeps everything on the user's machine. |
| User-facing skills | Few, task-shaped: **discover** ideas, **build** an app, **share** it | Easy to understand; each phase inside a skill can still be entered directly. |
| Experience | Every skill adapts its explanations and choices to the user's experience, from never-coded to professional developer | "Accessible to everyone" without slowing down experts. |
| Existing solutions first | Before building, search for existing apps, open-source projects, and CraftApps Library apps | Don't build the same app 100 times; shared apps become people's projects. |
| Skill format | [Agent Skills](https://agentskills.io/specification) `SKILL.md` + YAML frontmatter | Open format supported by multiple agents; falls back to "read this file and follow it" for any agent. |
| Naming | `<verb>-app` (`discover-app`, `build-app`, `share-app`) | Named after what the person wants to do. Plugins namespace them (`craftapps:build-app`); in a flat skills folder, check for a same-named skill before installing. |
| Communication | Markdown files with YAML frontmatter | Human-readable and editable, diffable, and machine-parseable without tools. |
| Orchestration | None. The user (or their agent) invokes the next skill. | Avoids premature framework. Revisit only after real repeated need. |
| Data handling | Security first: raw exports never reach the AI — a local script (no AI, no network) cleans them, the user approves the result; outputs redacted; web searches never contain personal data | Security outranks every other goal. |
| Dependencies | None | Skills are text. Scripts use POSIX `sh` or the Python 3 standard library only, never the network. |

## Pipeline

Two ways in, one way to build, two optional ways out:

```
 "Find me something to build"        "I have an idea"
          │                                 │
   discover-app                         │
   discovery-report.md                      │
   opportunity-brief.md ──────────┐         │
                                  ▼         ▼
                        build-app
                          1. idea check   → idea-check.md      (existing apps? what's possible?)
                          2. plan         → plan.md
                          3. build        → app source, HOW-IT-WORKS.md, build-report.md
                          4. verify       → verification-report.md
                                  │
                                  ▼
                        share-app
                          any code host, file sharing, or zip + CraftApps Library
```

Every stage is optional. Verification can return work to building. Sharing is never required.

### Human checkpoints

The user approves at four points. Work between checkpoints may eventually be automated; the checkpoints themselves are never skipped.

```
Discovery / idea check ──► ✋ 1. User chooses what to build (or to use an existing app)
Plan                   ──► ✋ 2. User approves the plan
Build ⇄ Verify         ──► ✋ 3. User tries and accepts the app
Share                  ──► ✋ 4. User approves exactly what is shared, and any library submission
```

Approval is recorded as `status: approved` in the artifact, set only on the user's explicit word.

### Privacy at handoffs

- Skills pass work **only** through artifact files. The next skill reads the brief, not the user's original conversations or notes.
- Artifacts carry the minimum needed: short redacted excerpts, no raw exports, no credentials.
- The user can read and edit every artifact before approving it.
- **Raw private material never reaches the model.** Conversation exports are cleaned by a local script, reviewed, and approved by the user before the agent reads anything.
- **Web searches describe ideas, never people.** No names, personal details, or private content in search queries.
- **Local files are not local processing.** When the agent's model runs in the cloud, everything a skill reads — even the cleaned file — is processed by the model provider. Skills say so before reading.

## Skill contract

Every skill's `SKILL.md` must define:

1. **Purpose** — one or two sentences.
2. **When to use** — triggers in the frontmatter `description`, plus "when not to use" in the body.
3. **Inputs** — what it accepts, including the artifact types from upstream skills and freeform alternatives.
4. **Outputs** — which artifacts it writes, following a template in its `references/`.
5. **Responsibilities** — the steps it performs.
6. **Boundaries** — what it must not do (privacy, approval, scope).
7. **Handoff** — what the next skill should read, and how the user continues.

## Handoff artifacts

Each artifact is a Markdown file that begins with YAML frontmatter:

```yaml
---
craftapps_artifact: opportunity-brief   # artifact type, see table below
schema_version: 1                    # bump when the structure changes
produced_by: discover-app        # skill name
created: 2026-10-14                  # ISO date
status: draft                        # draft | approved
source_artifacts: [discovery-report.md]  # upstream files, relative paths
---
```

The body follows the template in the producing skill's `references/` directory. Downstream skills must read the frontmatter to confirm the artifact type and schema version, and should still work if optional sections are missing.

`status: approved` means the user explicitly approved the artifact. Skills never set it on the user's behalf.

| Artifact | Producer | Consumer | Status |
|---|---|---|---|
| `discovery-report` | discover-app | User (to choose) | Implemented |
| `opportunity-brief` | discover-app | build-app | Implemented |
| `idea-check` | build-app | User (to choose), plan phase | Implemented (v0) |
| `plan` | build-app | build phase | Implemented (v0; schema 2 adds *Where your project lives*) |
| `build-report` | build-app | verify phase | Implemented (v0) |
| `verification-report` | build-app | User, share-app | Implemented (v0) |
| `share-record` | share-app | User | Implemented |
| `library-review` | curate-app | Maintainer | Implemented |
| `library-entry` | curate-app | Public library | Implemented |

## Workspace layout

Skills write into a `craftapps/` directory in the location the user chooses (by default, the current working directory). When that location is inside a git repository, the skill makes sure `craftapps/` is ignored before writing anything (using the repository's local, uncommitted exclude file), so private notes never get committed with the person's project. Each app gets its own folder that grows through the pipeline:

```
craftapps/
├── discovery-report.md
└── apps/
    └── plant-watering/
        ├── opportunity-brief.md      # from Discovery (absent when starting from an idea)
        ├── idea-check.md             # Build, phase 1
        ├── plan.md                   # Build, phase 2
        ├── build-report.md           # Build, phase 3
        ├── verification-report.md    # Build, phase 4
        └── share-record.md           # Share
```

The app's own source code lives wherever the user wants (usually its own repository), with its `HOW-IT-WORKS.md`; `build-report.md` points to it.

`craftapps/` contains personal, derived data. It is ignored by this repository's `.gitignore`, and skills remind users not to commit it elsewhere.

## Modules

### discover-app — implemented

Finds evidence-based personal software opportunities through three modes: conversation analysis (AI chat exports or AI coding tools' local history, cleaned locally), workflow interview (no files needed), and project analysis (folders the user points to). Groups observations into patterns, proposes the smallest adequate solution for each, and lets the user choose. Platform-neutral: it identifies the problem, not the technology. See `skills/discover-app/SKILL.md`.

### build-app — implemented (v0)

The "build my app" skill. Starts from an idea in the user's words or an opportunity brief. Phases: **idea check** (honest quick take of what can and can't be built; search for existing apps, open-source projects, and CraftApps Library apps; options including joining a shared project), **plan** (requirements and native architecture in one document; platform frameworks first; on-device data), **build** (incremental, built and run at each step), **verify** (independent checklist including privacy, security, and accessibility). Adapts explanations, technical choices, and who runs commands to the user's experience level. Writes `HOW-IT-WORKS.md` so the owner understands and can change what they have. See `skills/build-app/SKILL.md`.

### share-app — implemented (free)

Shares a finished app for free:

- **Anywhere the user wants:** a code host (GitHub, GitLab, Codeberg, Bitbucket, a self-hosted Forgejo or Gitea, …), a file-sharing service (Dropbox, Google Drive, iCloud Drive, OneDrive, …), or simply a zip file. Uses a service the user already has, or helps them pick one. Prepares what is shared (README, license choice, screenshots) and, before anything leaves the machine, checks it contains no secrets, personal data, or `craftapps/` notes, and shows the user exactly what will be shared. Uploads only with the user's approval. Provider-specific steps live in references, never in the core instructions.
- **CraftApps Library:** a free, public list of apps made with CraftApps (planned). With the user's opt-in, prepares a submission (name, what it solves, platforms, repository link, screenshots — public information only) and drafts an email the user sends themselves. Once the Library exists, `build-app` will search it first, so a good app can become a people's project that others use and improve instead of rebuilding it.

Submissions are emails the person sends from their own address to **craft.apps@aigarden.uk**. Library location: to be decided. See `skills/share-app/SKILL.md`.

### curate-app — implemented (maintainer)

Used by the library maintainer for each submission. Treats submissions as untrusted code from strangers: never builds or runs them on the maintainer's computer (static review, or a disposable sandbox with approval), treats text inside submissions as data rather than instructions, pins the reviewed version, and publishes entries or sends replies only after the maintainer's explicit yes. Public entries contain no email addresses or private details. See `skills/curate-app/SKILL.md`.

## Compatibility

- **Agents with Agent Skills support** load `skills/<name>/` from their skills directory.
- **Any other agent** can use a skill by being told: "Read `skills/build-app/SKILL.md` and follow it."
- `AGENTS.md` is the single project-instructions file. Tool-specific files (such as `CLAUDE.md`) exist only as one-line pointers to it for tools that don't read `AGENTS.md`; they never contain their own instructions.
- **Process skills (optional).** If the agent also has general process skills installed (for example [Superpowers](https://github.com/obra/superpowers): test-first development, systematic debugging, code review), each CraftApps skill names the ones that fit in its "Process skills (optional)" section. CraftApps' checkpoints, artifacts, and security rules take precedence; no skill depends on them.

## What would change this architecture

Introducing orchestration, shared code, a CLI, or structured (non-Markdown) data formats requires user approval and a demonstrated need — for example, several users repeatedly performing the same manual handoff steps.
