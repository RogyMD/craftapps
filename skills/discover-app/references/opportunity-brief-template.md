# Opportunity brief template

Write one brief per opportunity the user chooses, at `craftapps/apps/<slug>/opportunity-brief.md`. `<slug>` is a short lowercase-hyphenated name (e.g. `release-notes-pipeline`).

The brief is the handoff to `build-app`. It must stand on its own: a reader who has not seen the discovery report should understand the problem, the evidence, and the user's intent.

````markdown
---
craftapps_artifact: opportunity-brief
schema_version: 1
produced_by: discover-app
created: YYYY-MM-DD
status: draft            # set to approved only after the user explicitly approves
source_artifacts: [../../discovery-report.md]
opportunity_id: OPP-<n>
recommended_rung: <0–4>
target_devices: [<e.g. Mac>]   # where the solution runs; chosen from the user's devices
---

# <Opportunity name>

## Problem

<!-- The underlying job and why it matters to this user. 2–4 sentences. -->

## Evidence

<!-- Key observations with dates and short redacted excerpts. Label Observed/Inferred. -->

## Current workaround

<!-- How the user handles it today, step by step if known. -->

## Proposed direction

<!-- The recommended rung and solution, in a paragraph. This is a direction, not requirements. -->

## Out of scope

<!-- Things that came up but should not be part of the first version. -->

## Constraints and preferences

<!-- User's devices and why the target device fits; tools the user already uses; coding skills; privacy requirements; budget (e.g. "no subscriptions"). Native solutions only — no websites or hosted services. Label Observed/Assumed. -->

## Open questions

<!-- What the build stage must ask the user. -->

## Privacy

<!-- Data touched, local processing, credentials. -->
````
