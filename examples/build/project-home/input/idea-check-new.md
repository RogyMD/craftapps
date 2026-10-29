---
craftapps_artifact: idea-check
schema_version: 1
produced_by: build-app
created: 2026-10-15
status: approved
source_artifacts: []
experience: new
user_devices: [iPhone]
web_search: done
---

<!-- SYNTHETIC EXAMPLE: fictional person; app names in "Existing solutions" are invented for illustration. -->

# Idea check: Plant watering helper

## The idea

> "I keep forgetting to water my plants, and they all need water at different times. I want my phone to remind me, and to tick off when I've done it."

The problem: different plants need water on different schedules, and remembering them all is hard.

## Quick take

- **Can build:** an iPhone app where you add each plant with how often it needs water, get a reminder when one is due, and tap to mark it watered. Everything stays on your phone.
- **Can't / hard:** the app can't know whether the soil is actually dry. It only follows the schedule you set.
- **Needs:** a Mac with Xcode (free) to build it, and your free Apple ID to put it on your iPhone. Apps installed this way need a quick refresh every 7 days unless you join Apple's paid developer program.
- **Smaller alternative:** repeating reminders in the iPhone's Reminders app, one per plant. That's free and already on your phone, but there's no plant list and no history.

## Existing solutions

| Name | Type | What it does | Cost | Privacy | Fit |
|---|---|---|---|---|---|
| Reminders (built in) | Built-in feature | Repeating reminders | Free | On your devices and iCloud | Partial: no plant list |
| "LeafNote" | Store app | Plant care schedules, plant identification | Subscription for more than 5 plants | Account required | Good, but subscription and account |
| "open-plant-log" | Open source | Watering schedules for Android | Free | Local | Wrong device (Android only) |

No CraftApps Library project found.

## Options

- **Use Reminders:** free and instant, but your plants aren't listed in one place.
- **Use LeafNote:** works well, but costs a subscription and needs an account.
- **Build your own:** free, private, exactly how you want it. Takes an afternoon with my help, and you'll own it.

## Recommendation

Build your own small iPhone app. You want something simple that doesn't need an account or subscription, and it's a great first app to own. Once it works, you could share it in the CraftApps Library so others with the same problem don't have to build it again.

## Decision

The user chose to build their own app (2026-10-15).
