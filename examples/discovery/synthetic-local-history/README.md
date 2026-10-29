# Fixture: local AI history (conversation scenarios)

**All scenarios are synthetic.** No files: each scenario is a short situation given to a fresh agent together with the `discover-app` skill. They test how the skill talks to the person around their local AI tool history, not the analysis itself.

The cleanup of Claude Code and Codex session logs is tested separately with synthetic logs built inside `scripts/test_prepare_input.py`.

## How to run

For each scenario in [`expected-findings.md`](expected-findings.md), start a fresh agent session, give it the `discover-app` skill folder and the scenario text, and tell it to run no commands and read nothing outside the skill folder. Ask for its actions and its exact messages to the person. Score them against the rubric and record the result in [`evaluations.md`](evaluations.md).
