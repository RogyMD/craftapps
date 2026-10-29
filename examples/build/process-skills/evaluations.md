# Evaluations — process skills

## 2026-10-15 — baseline (RED) and with the mapping (GREEN)

**Setup:** fresh subagents (one cloud LLM) in an agent with Superpowers installed and its "use skills" introduction loaded. RED runs had `build-app` without `references/process-skills.md` or the SKILL.md pointer; GREEN runs had both. Scored by the maintainer's session from each run's files and `process-log.md`. One run per scenario; web search not used.

| Item | RED | GREEN |
|---|---|---|
| A1 matching process skill used | ❌ rejected brainstorming entirely ("would add a second interview") | ✅ brainstorming, questioning only |
| A2 CraftApps Phase 1 in charge | ✅ | ✅ |
| A3 no stray spec file | ✅ | ✅ (explicitly skipped `docs/superpowers/specs/`) |
| A4 no jargon for the newcomer | ✅ | ✅ |
| A5 stopped at checkpoint | ✅ (three questions at once) | ✅ (one blocking question: "Do you have a Mac?") |
| B1 tests first | ✅ mostly; two tests added after the code | ⚠️ mostly; first implementation was more than minimal, so five tests passed immediately (disclosed) |
| B2 independent review | ❌ self-review only ("agents weren't requested") | ✅ `requesting-code-review` → separate read-only reviewer; **found a real bug** (days that start at 01:00 in Santiago, Beirut, Havana, Cairo, the Azores) |
| B3 root cause before fix | n/a (no unplanned failure) | ✅ `systematic-debugging`; failing tests first, then fix, then re-review |
| B4 verified before claiming | ✅ | ✅ |
| B5 no unagreed plan change | ❌ changed `isDue(on:)` to `isDue(on:in:)`, reported afterwards | ✅ kept `isDue(on:)` (calendar defaulted); open choices in `questions.md` |
| B6 artifacts in place, no pushes | ✅ | ✅ |

**Result:** RED A 4/5, B 4/5 (B3 n/a). GREEN A 5/5, B 5/6 + 1 partial (B1).

The baseline shows that with Superpowers loaded, agents already use test-first and verification on their own; the mapping's value is in the phases they skipped (questioning, independent review, root-cause debugging) and in CraftApps taking precedence over a process skill's own files and wording.

**Not tested:** `writing-plans` in Phase 2; `executing-plans`/`subagent-driven-development` on a multi-step plan; `finishing-a-development-branch`; the process-skills sections in `discover-app`, `share-app`, and `curate-app` (one or two lines each, mapping to `verification-before-completion` and, for curate batches, `dispatching-parallel-agents`); an agent *without* Superpowers (the sections are conditional and should be ignored).
