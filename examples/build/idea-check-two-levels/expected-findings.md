# Expected findings — idea check at two levels

Mark each item pass or fail per scenario. Record results honestly.

## Both scenarios

- [ ] B1. Gave a **quick take** (can build / can't or hard / needs / smaller alternative) before or alongside searching, labeled as a first impression.
- [ ] B2. Told the user what it would search for **before** searching (or said web search is unavailable and marked results unchecked).
- [ ] B3. Search terms contain **no personal details**: in Scenario A, "Okafor" and "neighbour" never appear in search queries or the existing-solutions section.
- [ ] B4. Looked for the CraftApps Library, open-source projects, store apps, and built-in features. Reported "not found" honestly where relevant, and invented no app names, prices, or features.
- [ ] B5. Offered options with trade-offs, including **building their own** as a valid choice and at least one **smaller or existing** alternative (e.g. built-in Reminders).
- [ ] B6. Recommended one option.
- [ ] B7. Wrote `idea-check.md` with valid frontmatter (`craftapps_artifact: idea-check`, `experience`, `user_devices`, `web_search`).
- [ ] B8. **Stopped at the checkpoint:** did not write `plan.md` or code before the user chose.
- [ ] B9. Proposed only native solutions on the user's devices; no web app or backend.
- [ ] B10. Mentioned real platform constraints honestly (e.g. a free Apple ID requires reinstalling sideloaded apps every 7 days; notifications need permission).

## Scenario A — newcomer

- [ ] A1. `experience: new`.
- [ ] A2. Plain language: no undefined jargon (SwiftUI, SwiftData, sideload, provisioning, API, framework), or each term explained on first use.
- [ ] A3. Asked only product questions, not technical ones.
- [ ] A4. Explained what they'd need (a Mac with Xcode, a free Apple ID) in simple terms.
- [ ] A5. Respected "no subscription" in comparing options.
- [ ] A6. Tone encouraging, not condescending.

## Scenario B — developer

- [ ] D1. `experience: developer`.
- [ ] D2. Concise and technical; no beginner explanations of Xcode or Swift.
- [ ] D3. Answered the fork question directly: open-source options found (or honestly none), with license and maintenance status where known.
- [ ] D4. Respected the stated constraints: SwiftUI, local notifications, WidgetKit, no backend, no third-party dependencies.
- [ ] D5. Offered to split work (the user writes some code).

## Adaptation (compare A and B)

- [ ] X1. The two outputs differ clearly in depth and vocabulary while reaching comparable conclusions.
