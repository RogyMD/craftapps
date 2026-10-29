---
name: build-app
description: Use when a person describes an app, tool, or automation idea they want built for themselves — "I want an app that…", "build my app", "can you make me a tool to…", "is this possible?" — or hands over a CraftApps opportunity brief. For any experience level, from people who have never coded to professional developers. Part of CraftApps.
---

# Build App

Turn a person's idea into software they own: check the idea, say honestly what can be built, plan it, build it, verify it. **Adapt every step to the person's experience** — a first-timer and a senior developer get the same quality of result, explained very differently.

**Security first.** Never put personal data into web searches. Build apps that keep data on the device, with no tracking or analytics, secrets in the platform's secure storage, and network access only when a feature requires it. Ask before installing anything or touching files outside the project folder.

**Don't build the same app 100 times.** Before building, look for an existing app or a CraftApps project that already solves it. Joining or improving a shared project is often better than starting another.

## When not to use

- The person has no idea yet and wants suggestions → use `discover-app`.
- The person wants to publish to app stores → not covered by CraftApps. Point them to the store's official guide and never handle their store passwords.
- Sharing the app anywhere (a code host, Dropbox or similar, a zip file) or submitting it to the CraftApps Library → `share-app`.

## Inputs

Either an idea in the user's own words, or an `opportunity-brief.md` from `discover-app` (skip the idea interview; still do the existing-solution check).

## Outputs

All in `craftapps/apps/<slug>/` (where `<slug>` is a short hyphenated name):

| Phase | Artifact | Template |
|---|---|---|
| 1. Idea check | `idea-check.md` | [references/idea-check.md](references/idea-check.md) |
| 2. Plan | `plan.md` | [references/plan.md](references/plan.md) |
| 3–4. Build + verify | `build-report.md`, `verification-report.md`, the app's source, and `HOW-IT-WORKS.md` in the app folder | [references/build-and-verify.md](references/build-and-verify.md) |

**Keep `craftapps/` out of git — before the first file is written.** It holds private notes about the person. If the folder you will write in is inside a git repository (`git rev-parse --show-toplevel` succeeds there):

1. Run `git check-ignore -q craftapps/`. If it is already ignored, go on.
2. If not, append the line `craftapps/` to the repository's local exclude file (its path is printed by `git rev-parse --git-path info/exclude`). That file is never committed, so the person's own `.gitignore` and project stay untouched. Edit `.gitignore` only if the person asks.
3. Run `git check-ignore -q craftapps/` again to confirm. If you cannot make it ignored, ask the person for a folder outside the repository and write there.
4. Tell the person in one plain sentence where their private notes are and that they are kept out of their project's history.

Example: [examples/sample-idea-check.md](examples/sample-idea-check.md).

## Adapting to the person

Before anything else, work out their experience level and devices (one short question if unclear). Then follow [references/experience-levels.md](references/experience-levels.md) for how much to explain, who makes technical choices, and who runs commands. Switch levels whenever they ask ("explain more", "skip the details") or their answers show you misjudged.

## Process

Each phase ends at a checkpoint. **Do not start the next phase until the user explicitly agrees.** The user may stop after any phase, or enter at a later phase if they already have a plan or code.

### Phase 1 — Idea check

1. **Listen.** Let them describe the idea; ask only what is needed to understand the problem (a few questions at a time).
2. **Quick take.** Immediately give an honest first answer from your own knowledge: can this be built, roughly what it would do, on which of their devices, and anything that is impossible or hard (platform limits, data that apps cannot access). Label it as a first impression.
3. **Send the quick take and a one-line search plan to the user, then search** for existing solutions, following the reference. Never search before the user has seen what you will search for. Search terms describe the idea only, never personal details.
4. **Report options** honestly: use an existing app, join or improve an existing open project, fork one, or build their own — with the trade-offs (privacy, cost, subscriptions, ownership). Building their own is a valid choice even when apps exist.
5. Write `idea-check.md`. **Checkpoint:** the user chooses a direction.

### Phase 2 — Plan

Write `plan.md` using the template: what the first version does (and doesn't), how it's used, platform and technology, data and storage, where the project lives (its folder on this computer and an optional private backup), privacy and security, dependencies (each justified), and build steps. Prefer the smallest solution: an automation instead of an app when that is enough. **Checkpoint:** the user approves the plan.

### Phase 3 — Build

Build incrementally per [references/build-and-verify.md](references/build-and-verify.md): small steps, build and run after each, fix errors, keep the user informed at their level. Write `HOW-IT-WORKS.md` for the owner. Report only what you actually built and ran.

### Phase 4 — Verify

Verify against the plan using the checklist in the same reference — ideally in a fresh session or with a fresh read of the code, not from memory. Fix what fails, re-verify, and write `verification-report.md`. **Checkpoint:** the user tries the app and accepts it. Then explain how to run it, where its data lives, and how to share it if they want (a code host, a file-sharing service like Dropbox, a zip file, or the CraftApps Library — always optional).

## Process skills (optional)

If your agent has general process skills installed (for example Superpowers: test-first development, systematic debugging, code review), use the matching one in each phase — see [references/process-skills.md](references/process-skills.md). CraftApps' checkpoints, artifacts, security rules, and plain language for newcomers always take precedence.

## Boundaries

- Never claim something works without having built and run it. Say what was not tested.
- Never add accounts, subscriptions, servers, analytics, ads, or tracking unless the user explicitly asks and understands the trade-off.
- Never commit secrets. Never push, publish, or send anything without explicit approval.
- Never install tools, change system settings, or delete files outside the project without asking first.
- Respect the licenses of existing projects you build on or contribute to.

## Common mistakes

| Mistake | Fix |
|---|---|
| Starting to code right after hearing the idea | Phase 1 first: quick take, search, options, checkpoint |
| Skipping the search because "I know how to build this" | The search is about whether it *should* be built, not whether you can |
| Jargon with a first-timer; hand-holding a senior developer | Follow the experience-level reference |
| A web app or backend "because it's easier" | Native app or automation on the user's own devices |
| Adding a library for something the platform already does | Platform frameworks first; justify every dependency in the plan |
| "It's done" without running it | Build, run, verify; report what was and wasn't tested |
| Including personal details in search queries | Describe the idea generically |
