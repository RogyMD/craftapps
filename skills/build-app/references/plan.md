# Phase 2 — Plan

The plan combines *what* to build (requirements) and *how* (architecture) in one short document the user approves.

## Principles

- **Smallest first version** that solves the problem. Everything else goes under "Later".
- **Native to the user's devices.** No websites or hosted backends.
- **Platform frameworks first.** Every third-party dependency needs a written reason: what it does that the platform cannot, and its license.
- **Data stays on the device** unless the user needs sync; then prefer the platform's own sync (for example iCloud for Apple devices) over a custom server.
- **Secure by default:** secrets in the platform's secure storage, minimum permissions, no analytics or tracking, network only when a feature requires it.
- **Accessible:** system text sizes, screen readers, sufficient contrast, no information conveyed by color alone.
- **The person knows where their project lives.** Name the folder on this computer for the app's source code, and ask whether they want a backup copy somewhere else. Ask it as a question, with "no backup" as one of the answers — an account they mention is not a yes. Offer only places that fit what you know about them: a **private** repository on a code host they already use, a zipped copy in a cloud drive they already use, or no backup (the code then exists only on this computer; say so plainly). Write their answer in the plan; until they answer, it says "waiting for your answer". Any online copy is private: making it public is `share-app`'s job. Don't keep the project itself inside a synced cloud folder (syncing can damage a git project); back up a zipped copy instead. For things made on the device itself, such as a Shortcut, say where it lives instead.

## Default technology by platform

Starting points, not rules. Follow a developer's preferences when they have them.

| Target | Default | Local storage |
|---|---|---|
| iPhone, iPad, Mac, Apple Watch | Swift + SwiftUI | SwiftData, or files / UserDefaults for small data |
| Android | Kotlin + Jetpack Compose | Room, or DataStore for small data |
| Windows | C# + WinUI 3 | Local files / SQLite via the platform |
| Linux desktop | GTK 4 (language per user preference) | Local files / SQLite |
| Several platforms at once | Separate native apps if the app is small; otherwise discuss a cross-platform framework and its trade-offs with the user | Per platform |
| Automation | Platform script (shell, PowerShell, Python standard library), Apple Shortcuts, or a scheduled task | Files |

Before choosing, check the user has (or can install) the required tools — Xcode needs a Mac; Android Studio runs on Mac, Windows, and Linux.

## plan.md template

Adapt the depth to the experience level (see experience-levels.md); keep all sections.

````markdown
---
craftapps_artifact: plan
schema_version: 2
produced_by: build-app
created: YYYY-MM-DD
status: draft            # approved only on the user's explicit word
source_artifacts: [idea-check.md]
target_devices: [<e.g. iPhone>]
experience: new | some | developer
---

# Plan: <app name>

## What the first version does
<!-- 3–7 bullet points, each a user-visible capability. -->

## Not in the first version
<!-- Ideas deliberately left for later. -->

## How it's used
<!-- The main flow, step by step, from opening the app to finishing the task. -->

## Platform and technology
<!-- Target devices, language/framework, and why. One paragraph for a newcomer. -->

## Data and storage
<!-- What is stored, where (on device), and how the user can export or delete it. -->

## Where your project lives
<!-- The folder on this computer for the source code (a specific path the person can change), and the backup they chose: none, a private repository on <code host>, or a zipped copy in <cloud drive folder>. For a newcomer, in plain words: "Your app's code will be in Documents/PlantPal on your Mac. Want a private backup copy in your iCloud Drive, in case anything happens to your Mac?" -->

## Privacy and security
<!-- Permissions needed and why; network use (if any) and why; where secrets live; "no analytics or tracking". -->

## Dependencies
<!-- "None" is the goal. Otherwise: name, why the platform can't do it, license. -->

## Build steps
<!-- Ordered, small, each producing something that runs. -->

## What you'll need
<!-- Tools to install, accounts (e.g. a free Apple ID to run on your own iPhone), time estimate. -->
````
