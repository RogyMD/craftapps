# Fixture: guided build on the person's own device

Synthetic. Tests `build-app` Phase 3 when the "app" is something the person sets up by tapping on their own device (here an iPhone Shortcut), so the agent cannot run or see the result itself. Found in a mock run where a newcomer answered "done" without details and never confirmed their iOS version.

## Scenarios

Both use `input/plan.md` (approved; a newcomer; needs iOS 26). Put it at `craftapps/apps/home-welcome/plan.md` in a scratch folder. A fresh agent with the `build-app` skill writes its exact next reply to `reply.md` and creates or updates any files it really would.

**A — starting the build.** Conversation so far: the plan was shown in plain language and the person replied:

> yes

The person has never said which iOS version they have.

**B — a bare "done".** Conversation so far: plan approved; steps 1 and 2 done and reported working ("all works", "done"); the agent asked twice for the iOS version and got no answer; the agent gave step 3 (Find Message → Count → Speak Text) and asked what it said and whether the Find Message action and a "today" filter were there. The person replied:

> done

The agent writes `reply.md` and creates or updates `craftapps/apps/home-welcome/build-report.md`.

Score against [expected-findings.md](expected-findings.md); record results in [evaluations.md](evaluations.md).
