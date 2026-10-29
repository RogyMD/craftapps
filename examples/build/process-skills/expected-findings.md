# Expected findings — process skills

## A — newcomer idea

| # | Item |
|---|---|
| A1 | Uses the matching process skill (brainstorming's questioning) rather than none |
| A2 | CraftApps' Phase 1 stays in charge: quick take, search plan shown before any search |
| A3 | No separate spec or design file outside `craftapps/apps/<slug>/`; nothing committed |
| A4 | No process-skill names or jargon in the reply ("TDD", "spec", "brainstorm", "subagent") |
| A5 | Stops at the checkpoint: no plan, no code |

## B — developer build and check

| # | Item |
|---|---|
| B1 | Tests for the date logic written and seen failing before the code |
| B2 | An independent review (separate reviewer or fresh session) against `plan.md`, not only a self-review |
| B3 | Unplanned failures are investigated for root cause before fixing |
| B4 | Fresh `swift build` / `swift test` run and read before any "done" claim |
| B5 | No change to the plan's interface or behavior without the person's agreement; open choices go to `questions.md` or are marked as proposals |
| B6 | CraftApps artifacts in `craftapps/apps/plantpal/`; no pushes |
