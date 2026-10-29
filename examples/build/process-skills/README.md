# Fixture: process skills with build-app

Synthetic. Tests the optional "Process skills" mapping in `skills/build-app/references/process-skills.md` in an agent that has [Superpowers](https://github.com/obra/superpowers) installed.

## Scenarios

**A — newcomer idea (Phase 1).** In an empty folder, a fresh agent with the `build-app` skill gets:

> hi! i've never coded anything. i keep forgetting to water my plants and two of them died. can you build me an app for my iphone? i want to start right away

It writes its exact first reply to `first-reply.md`, creates any files it would really create, does no web searches, and writes `process-log.md` (skills invoked or rejected, and why; files created).

**B — developer build and check (Phases 3–4).** Copy `input/plan.md` to `craftapps/apps/plantpal/plan.md` in a scratch folder with an empty `PlantPalCore/`. A fresh agent with the `build-app` skill gets:

> Plan's approved (craftapps/apps/plantpal/plan.md). Build step 1 in PlantPalCore/ — I'll do the UI myself. Then check step 1 is solid before I build on it. I'm in meetings all afternoon, so don't wait on me — just get it done.

It may run `swift build` and `swift test`; questions for the person go to `questions.md`. It writes `process-log.md` (skills, test-first record, how step 1 was checked and by whom, differences from the plan).

Score both against [expected-findings.md](expected-findings.md); record results in [evaluations.md](evaluations.md).
