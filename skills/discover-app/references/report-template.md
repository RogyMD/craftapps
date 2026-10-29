# Discovery report template

Copy the structure below into `craftapps/discovery-report.md`. Keep section order. Delete instructional comments (`<!-- -->`). Omit a section only if noted as optional.

````markdown
---
craftapps_artifact: discovery-report
schema_version: 1
produced_by: discover-app
created: YYYY-MM-DD
status: draft
sources:
  - path: <path as provided by the user>
    kind: cleaned-export | notes | workflow | app-list | project | interview | other
    cleaned_locally: true | false   # true when passed through scripts/prepare_input.py and approved by the user
    coverage: <e.g. "all user messages, 48 conversations" or "sample: 120 of 900">
    date_range: YYYY-MM-DD..YYYY-MM-DD
excluded: [<topics, people, or ranges the user excluded>]
user_devices: [<e.g. iPhone, Mac>]   # as stated by the user, or inferred from the material and marked "(inferred)"; empty if unknown
---

# Discovery Report

## Summary

<!-- 3–5 sentences: what was analyzed, the strongest patterns, and the top recommendation. -->

## At a glance

<!-- One row per opportunity, same order as below. Values per assessment-rules.md. -->

| ID | Opportunity | Frequency | Cost today | Complexity | Value | Evidence | Suggested solution |
|---|---|---|---|---|---|---|---|

## Scope and coverage

<!-- What was read, what was sampled or skipped and why, and limitations (e.g. missing dates). -->

## Opportunities

<!-- Ranked by assessment-rules.md. Repeat this block per opportunity. 3–7 typical; zero is fine. -->

### OPP-1: <short name>

- **Problem:** <the underlying job, in the user's terms>
- **Evidence:** <observation IDs and one-line descriptions; label Observed/Inferred>
  > "<short verbatim excerpt>" — <source, date>
- **Frequency:** <per assessment-rules.md>
- **Cost today:** High | Medium | Low — <time and frustration per occurrence>
- **Recommended solution:** Rung <0–4> — <one-paragraph description, naming the target device(s) for rungs 2–4>
- **Why this rung:** <why lower rungs are insufficient, or why this rung is enough>
- **Alternatives considered:** <other rungs or existing tools, briefly>
- **Value:** High | Medium | Low — <reason>
- **Complexity:** XS | S | M | L — <main risk>
- **Evidence strength:** Strong | Moderate
- **Privacy:** <data touched, local or not, credentials>
- **Assumptions to confirm:** <Assumed items, or "none">

## Weak signals

<!-- Single mentions, generic ideas, or patterns without enough evidence. One line each with the reason it was not promoted. -->

| Signal | Observations | Why not an opportunity |
|---|---|---|

## Observations

<!-- Every observation referenced above. Excerpts short and redacted. -->

| ID | Date | Source | Type | Excerpt or summary |
|---|---|---|---|---|

## Privacy notes

<!-- Redactions made; credentials or sensitive data noticed in the input (without repeating them); reminder that this report contains personal data. -->

## Next step

Which opportunities would you like to explore? Reply with IDs (e.g. "OPP-1 and OPP-3"), "none", or questions. Chosen opportunities get an opportunity brief that a requirements step or a coding agent can build on.
````
