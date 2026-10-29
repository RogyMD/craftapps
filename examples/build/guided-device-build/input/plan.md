---
craftapps_artifact: plan
schema_version: 2
produced_by: build-app
created: 2026-10-16
status: approved
source_artifacts: [idea-check.md]
target_devices: [iPhone]
experience: new
---

# Plan: Home Welcome

> Synthetic fixture. No real personal data.

## What the first version does

- When the iPhone arrives home, the Hue lights turn green by themselves.
- The iPhone then says out loud how many emails arrived today and who the first three are from.
- If there were no emails, it says "Welcome home. No new emails today."
- It can also be run any time by tapping it.

## Not in the first version

- Reading every email in full; AI-written summaries; lights only after dark.

## How it's used

1. You come home. Nothing to do.
2. As your phone gets near home, the lights turn green.
3. Your phone speaks the email summary.

## Platform and technology

A **Shortcut** in the iPhone's Shortcuts app, plus an **automation** that runs it when you arrive home. It turns on a green "Welcome" scene through Apple's Home app, finds today's emails with the Mail "Find Message" action, and speaks a sentence with "Speak Text". No app, no code.

## Data and storage

Nothing new is stored. To remove everything, delete the shortcut and the automation.

## Where your project lives

On your iPhone, in the Shortcuts app. There is no code folder on a computer.

## Privacy and security

Permissions: location, Home, Mail. No network of its own. Emails never leave the phone. No analytics or tracking.

## Dependencies

None.

## Build steps

1. Get ready: Gmail added to Apple Mail; Hue Bridge added to the Home app; a green scene "Welcome". *Try:* tap the scene.
2. Shortcut "Welcome Home" turns on the Welcome scene. *Try:* tap it.
3. Find today's emails, count them, speak "You got N emails today." *Try:* tap it and listen.
4. Add the first three senders and the "no emails" case. *Try:* tap it and listen.
5. Automation "When I arrive home → run Welcome Home", set to run immediately. *Try:* a short walk.
6. `HOW-IT-WORKS.md`.

## What you'll need

- An iPhone with **iOS 26 or later**: the Mail "Find Message" action was added in iOS 26. (Run-immediately automations need iOS 17 or later.)
- A Hue Bridge and the Hue app, already set up.
- About 30–45 minutes.
