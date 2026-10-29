# Process skills (optional)

Some agents have general **process skills** installed — reusable working methods such as test-first development or systematic debugging. One widely used set is [Superpowers](https://github.com/obra/superpowers). If those skills are available to you, use the matching one at each phase below. If they are not, follow this skill's own instructions; nothing here is required.

## CraftApps rules come first

A process skill shapes *how* you work inside a phase. It never replaces the phase:

- **Checkpoints and artifacts stay CraftApps'.** Write `idea-check.md`, `plan.md`, `build-report.md`, and `verification-report.md` in `craftapps/apps/<slug>/` using this skill's templates. Do not create separate spec or plan files elsewhere, and do not commit them to the app's repository.
- **Security and privacy rules stay in force.** No process skill permits searching with personal details, installing without asking, pushing, or publishing.
- **The person's level decides the words.** Never name process skills or their jargon to newcomers ("TDD", "worktree", "subagent"). Use them silently; report results in plain language.
- **Plan changes need the person's agreement.** If a process skill or the code suggests something different from the approved plan (a renamed function, a changed signature, a dropped item), stop and propose the change first. Reporting it afterwards is not agreement.

## Which skill when

| Phase | Use (Superpowers name) | How it fits |
|---|---|---|
| 1. Idea check | `brainstorming` — its questioning only | Ask one question at a time, offer 2–3 approaches with trade-offs. Its design document becomes `idea-check.md`; the existing-solution search still happens. |
| 2. Plan | `writing-plans` | Use its small, testable steps to fill `plan.md`'s build steps (developer level: exact files and test commands). Save only `plan.md`. |
| 3. Build | `test-driven-development` | For logic that can break silently: write the test, see it fail, then write the code. |
| 3. Build | `executing-plans` or `subagent-driven-development` | Work through `plan.md`'s steps in order, with this skill's build loop. Use subagents only if your agent supports them. |
| 3. Build | `systematic-debugging` | Any build error, failing test, or crash you did not plan: find the root cause before changing code. |
| 4. Verify | `requesting-code-review` | This is the "separate reviewer" the verification checklist asks for: an independent review against `plan.md` before `verification-report.md`. |
| 4. Verify | `verification-before-completion` | Run the commands and read their output before saying anything works. |
| After acceptance | `finishing-a-development-branch` | Only if the app uses git branches; local commits only, never push without approval. |
