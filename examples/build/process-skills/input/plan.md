---
craftapps_artifact: plan
schema_version: 2
produced_by: build-app
created: 2026-10-15
status: approved
source_artifacts: [idea-check.md]
target_devices: [iPhone]
experience: developer
---

# Plan: PlantPal

<!-- Synthetic test fixture. -->

## What the first version does
- List plants with a watering interval in days.
- Show which plants are due today.
- Tap to mark watered.
- Local notification when a plant becomes due.

## Not in the first version
- Sync, photos, widgets.

## Platform and technology
SwiftUI app; core logic in a Swift package `PlantPalCore` (no dependencies) so it can be tested with `swift test`.

## Data and storage
SwiftData on device.

## Where your project lives
`~/Developer/PlantPal`, its own git repository. Backup: none (the developer's choice).

## Privacy and security
No network. Notification permission only.

## Dependencies
None.

## Build steps
1. `PlantPalCore`: watering schedule logic — next due date from last-watered date and interval (calendar days, user's time zone), `isDue(on:)`, and due plants sorted by how overdue they are. Must handle DST changes and intervals of 0 or negative (reject).
2. SwiftUI list and mark-watered.
3. Local notifications.
