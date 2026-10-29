# Roadmap

Status legend: ✅ done · 🚧 in progress · 📋 planned · 💭 proposed, not decided

## Milestone 0 — Foundation ✅

- Repository structure, `AGENTS.md`, `README.md`, vision and architecture docs.
- Skill contract, handoff artifact format, human checkpoints.
- Structural validation script.

## Milestone 1 — Discovery (v0.1) 🚧

Goal: prove that an agent can find *genuinely useful*, evidence-based personal software opportunities — ideally **one problem worth solving that the user had not recognized** — rather than a list of generic ideas.

Strategy: don't start by building an AI app builder. Start by building an AI that discovers which apps are worth building.

### Skill

- ✅ `discover-app` skill definition with three modes: conversation analysis, workflow interview, project analysis.
- ✅ Local cleanup script (`prepare_input.py`, stdlib only, no network): AI chat exports (ChatGPT and Claude formats so far; ZIP or folder) and text notes → user's messages only, redacted, for user review. Tested.
- ✅ Input support: cleaned exports, notes, interview answers, project folders.
- ✅ Cleanup of AI coding tools' local history (`--from claude-code`, `--from codex`): only what the person typed; tool output, shell commands, repeats, and sessions started by programs dropped; session index. Tested on synthetic logs and one real Claude Code history.
- ✅ Redaction: payment SDK keys; bank accounts (IBAN); every number of 13+ digits except timestamps; random keys in one letter case; paths, branch names, and UUIDs kept.
- ✅ Report with an at-a-glance score table (frequency, cost today, complexity, value, evidence) and the solution ladder (existing tool / prompt / automation / native app).
- ✅ Opportunity brief for handoff; user approval checkpoint.
- ✅ Privacy disclosure: local files are not local processing when the model is in the cloud.

### Evaluation

- ✅ Synthetic fixture (`examples/discovery/synthetic-ios-developer/`) with an expected-findings rubric.
- ✅ First blind run on the fixture (one cloud LLM): 26/27 rubric items, 1 partial — see `examples/discovery/synthetic-ios-developer/evaluations.md`.
- 📋 More runs for variance, with other LLMs (e.g. GPT, Gemini, a local open-weight model) and other agents.
- 📋 More export formats in the cleanup script (e.g. Gemini), driven by real demand.
- 📋 Fix findings from run 1: counting related complaints as incidents; which source path to record for cleaned exports.
- 📋 Maintainer self-test (results kept private; only redacted findings shared with consent):
  1. **Blind:** give it your conversations *without* mentioning your existing app ideas. What does it find?
  2. **Existing apps:** give it information about apps you've already built. Does it suggest useful improvements or complementary tools?
  3. **Someone else:** with their permission, give it another person's workflow (interview mode). Are the recommendations still useful?
- 📋 Use it for a week before building the next skill.
- 📋 More fixtures: a non-developer on Android/Windows; interview-only (no files); project analysis; a noisy large export; a case where the right answer is "nothing worth building".

### v0.1 release

- One excellent Discovery skill, a handful of examples, and a clear README.
- First public demo: *"I gave CraftApps my AI conversation history. Here's the personal software it suggested I build."*

Exit criteria: on fixtures, the skill finds the planted opportunities, rejects the traps, and redacts sensitive data; on real data, the maintainer judges at least one opportunity worth building that they had not already considered.

## Milestone 2 — Build my app 🚧

`build-app`: idea (or opportunity brief) → idea check → plan → build → verify, adapting to the user's experience from never-coded to professional developer. Replaces the earlier plan of four separate skills (Analyst, Architect, Developer, Verifier) with one task-shaped skill whose phases can be entered directly.

- ✅ v0 skill: idea check with existing-solution search (CraftApps Library apps, open source, store apps, built-in features), honest quick take, options including joining a shared project; plan template with native defaults per platform; build loop; verification checklist; owner's guide (`HOW-IT-WORKS.md`); experience-level guide.
- ✅ Fixture `examples/build/idea-check-two-levels/` (newcomer vs developer) with rubric.
- ✅ First evaluation of the idea check: newcomer 18/18, developer 17/18 — see `examples/build/idea-check-two-levels/evaluations.md`. Two fixes applied, not yet re-tested.
- ✅ Optional process skills (for example Superpowers: brainstorming, test-first, systematic debugging, code review) mapped to each phase in `references/process-skills.md`, with CraftApps' rules taking precedence; similar short sections in every skill. Tested RED → GREEN with `examples/build/process-skills/` (independent review found a real date bug the baseline missed).
- ✅ Private `craftapps/` folder kept out of the person's own git repositories (local exclude file, checked before writing), in `build-app` and `discover-app`. Tested RED → GREEN with `examples/build/private-folder-in-repo/`.
- ✅ The plan says where the app's code lives on the person's computer and asks whether they want a private backup (a private repository on their code host, a zipped copy in their cloud drive, or none). Plan `schema_version: 2`. Tested RED → GREEN → REFACTOR with `examples/build/project-home/`.
- ✅ Guided builds on the person's own device (an iPhone Shortcut the person taps in): regression fixture `examples/build/guided-device-build/`; the current skill passed without changes. A first guided mock run reached step 3 of 6.
- 📋 Evaluate a full build of a small app on Apple platforms (the maintainer can verify end to end), then Android and desktop.

## Milestone 3 — Share and the CraftApps Library 🚧

`share-app`: share an app wherever the user wants — any code host (GitHub, GitLab, Codeberg, self-hosted, …), a file-sharing service (Dropbox, Google Drive, iCloud Drive, OneDrive, …), or a zip file — always checked for secrets and personal data first, and, with the user's opt-in, submit it to the **CraftApps Library** (planned) — a free, public list of apps made with CraftApps. Submission via an email the user sends themselves. Once the Library exists, `build-app` will search it first, so popular apps become people's projects that others improve instead of rebuilding.

- ✅ `share-app` skill, tested RED → GREEN → REFACTOR with `examples/share/plantpal-traps/`.
- ✅ `curate-app` skill for the maintainer, tested RED → GREEN with `examples/curate/` (hostile and honest submissions).
- ✅ Submission address: craft.apps@aigarden.uk.
- 📋 Decide where the Library lives (e.g. a public repository with one entry per app).
- 📋 Library entry format: public information only — name, problem solved, platforms, repository link, license, screenshots.

## Later ideas (not committed)

- Supported integrations for additional input sources (always user-authorized).
- Lightweight evaluation tooling if manual rubric checks become a bottleneck.
