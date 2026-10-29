---
craftapps_artifact: idea-check
schema_version: 1
produced_by: build-app
created: 2026-10-18
status: approved
source_artifacts: []
experience: developer
user_devices: [Mac]
web_search: done
---

<!-- SYNTHETIC EXAMPLE: fictional person; app names in "Existing solutions" are invented for illustration. -->

# Idea check: Meeting-free focus timer for the Mac menu bar

## The idea

> "A menu bar timer that starts a 50-minute focus block, sets Focus mode, and logs the blocks to a CSV I can open in Numbers."

## Quick take

- **Can build:** a SwiftUI menu bar app (`MenuBarExtra`) with a timer, a Shortcuts call to toggle Focus, and a local CSV log.
- **Can't / hard:** apps can't set Focus modes directly; a Shortcut the user creates does it, and the app runs it.
- **Needs:** Xcode on the Mac.

## Existing solutions

| Name | Type | What it does | Cost | Privacy | Fit |
|---|---|---|---|---|---|
| "FocusBar" | Store app | Menu bar timer with stats | Subscription | Account for sync | Partial: no CSV, subscription |

No CraftApps Library project found.

## Decision

The user chose to build their own app (2026-10-18).
