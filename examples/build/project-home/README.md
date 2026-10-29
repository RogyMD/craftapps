# Fixture: where the person's project lives

Synthetic. Tests whether `build-app` settles, at the plan, where the app's source code will live on the person's computer and whether they want a private backup copy somewhere else. Without it, the code stays on one computer only, and nothing ever offers a backup: if the computer is lost, so is the app.

## Scenarios

A fresh agent with the `build-app` skill, opened in an empty scratch folder. It writes its exact next message to the person in `reply.md` and creates every file it really would (for example `craftapps/apps/<slug>/plan.md`). No web search.

**N — a newcomer at the plan.** Copy `input/idea-check-new.md` to `craftapps/apps/plant-watering/idea-check.md`. Conversation so far: the idea check was shown and the person replied:

> Let's build my own! I have a MacBook and my iPhone. I use iCloud Drive for my photos.

**V — a developer at the plan.** Copy `input/idea-check-developer.md` to `craftapps/apps/focus-timer/idea-check.md`. Conversation so far: the idea check was shown and the person replied:

> Build my own. I have a GitHub account. Go ahead and plan it.

Score against [expected-findings.md](expected-findings.md); record results in [evaluations.md](evaluations.md).
