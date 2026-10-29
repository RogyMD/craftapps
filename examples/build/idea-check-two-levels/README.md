# Fixture: idea check at two experience levels

**All people and details here are synthetic.**

Tests Phase 1 (idea check) of `build-app` — the part that decides *whether and what* to build — with two people who have similar ideas but very different experience. It does not test building.

## Scenario A — newcomer

The user says:

> I'm not technical at all, I've never made an app. I have about 15 houseplants and I keep forgetting to water them — my neighbour Mrs. Okafor waters them when I travel and she gets confused too. Could you make me something on my iPhone that reminds me which plant needs water and lets me tick it off? I don't want another subscription.

Pre-answered replies, if the agent asks: devices — iPhone only, a borrowed Mac is available; must-haves — reminders per plant, tick off; nice-to-have — a photo per plant; never — accounts, subscriptions.

## Scenario B — developer

The user says:

> I'm an iOS dev. I want a small SwiftUI app to track watering for my plants — per-plant intervals, local notifications, a widget showing what's due today. No backend, no third-party deps. Is there already something open source I should just fork?

Pre-answered replies, if the agent asks: devices — iPhone, Mac; fine with SwiftData; wants to write some code themselves.

## How to run

For each scenario, in a fresh agent session with `build-app` available, give the user's message, answer questions with the pre-answered replies, and approve nothing past the Phase 1 checkpoint. Score with [`expected-findings.md`](expected-findings.md).
