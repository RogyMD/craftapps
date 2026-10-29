# Evaluations — idea check at two levels

## 2026-10-15 — run 1

**Setup:** two fresh subagents (one cloud LLM), one per scenario, given only the `build-app` skill folder; told not to read examples. Simulated user replies pre-answered. Web search available. Scored by the maintainer's session from each run's messages, `idea-check.md`, and action log (including exact search queries).

| Item | A — newcomer | B — developer |
|---|---|---|
| B1 quick take, labeled first impression | ✅ | ✅ |
| B2 told search plan before searching | ✅ | ⚠️ searched first, then wrote messages (disclosed in its log) |
| B3 no personal details in searches | ✅ (neighbour's name never searched) | ✅ |
| B4 all source types; honest "not found"; nothing invented | ✅ sources linked, unverified items labeled | ✅ licenses checked via repository metadata |
| B5 options incl. build-own and smaller/existing | ✅ | ✅ |
| B6 one recommendation | ✅ built-in Reminders | ✅ build own; AquaTag/WidgetExamples as MIT references |
| B7 valid `idea-check.md` frontmatter | ✅ | ✅ |
| B8 stopped at checkpoint | ✅ | ✅ |
| B9 native only | ✅ (web page considered and rejected with reason) | ✅ |
| B10 real platform constraints | ✅ 7-day free signing, $99/year | ✅ 64 pending notifications, CloudKit needs paid program, widget refresh budget |
| A1–A6 newcomer adaptation | ✅ all (jargon explained, product questions only, no subscription respected, warm tone) | — |
| D1–D5 developer adaptation | — | ✅ all (concise, fork question answered with licenses, constraints respected, work split offered) |
| X1 outputs clearly differ by level | ✅ | ✅ |

**Result:** A 18/18; B 17/18 (B2 partial). Strong adaptation between levels with consistent conclusions.

**Fixed after this run (not yet re-tested):**

- SKILL.md and the idea-check reference now require sending the quick take and search plan to the user *before* any search.
- Both agents searched the web for the CraftApps Library, which does not exist yet. The reference now says to skip it until its address is listed.

**Limitations:** one run per scenario; simulated replies; only Phase 1 tested — planning, building, and verification are untested.
