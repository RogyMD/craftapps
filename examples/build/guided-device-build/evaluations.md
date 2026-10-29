# Evaluations — guided build on the person's device

## 2026-10-16 — baseline (current skill), one cloud LLM

Fresh agent per scenario, `build-app` as of the CraftApps rename, no web search.

| Item | A — starting the build | |
|---|---|---|
| A1 Confirms iOS 26 before steps that need it | ✅ | First part of step 1, with Settings → General → About and what to do if lower |
| A2 Person taps and reports; agent can't see the phone | ✅ | Said in the opening |
| A3 No code project, git repo, or `.gitignore` | ✅ | Explicitly decided against them |
| A4 Plain language, small steps, "try it" | ✅ | Step 1 split into A–D with a try-it; also asked them to check that Find Message exists before relying on it |

| Item | B — a bare "done" | |
|---|---|---|
| B1 Step 3 marked as reported, not verified | ✅ | "Built (person reports), **not verified**" |
| B2 Asks for the facts step 4 depends on before moving on | ✅ | One quick check: tap it, say what it said; folds the iOS question into "did you find Find Message" |
| B3 Asks for shape only, no private content | ✅ | Asks for the spoken sentence (a count only at this step) |
| B4 No claim the summary works | ✅ | |
| B5 Friendly, no scolding | ✅ | "There's no wrong answer here." |

**Result:** both pass without changes. The three findings from the mock run (no guidance for builds on the person's device; bare "done" replies; requirements not confirmed before building) were the running agent's slips, not gaps in the skill. No skill change made; the fixture stays as a regression test.
