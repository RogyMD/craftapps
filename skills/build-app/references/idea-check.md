# Phase 1 — Idea check

## Understand the idea

Ask only what you need (adapt wording to the experience level):

- What problem does this solve for you? When did you last run into it?
- What would you do with the app, step by step?
- Which devices should it run on? (Use the devices they actually own.)
- Must-haves versus nice-to-haves.
- Anything it must never do (share data, require an account, cost money)?

## Quick take

Before searching, give an honest first impression from your own knowledge:

- **Can build:** what a first version could realistically do, and on which devices.
- **Can't, or hard:** platform limits (for example, iPhone apps cannot read other apps' data or run freely in the background; some features need paid developer accounts or special permissions).
- **Needs:** tools to install, accounts, hardware, or the user's help.
- **Smaller alternative:** whether a Shortcut, script, or existing app feature might be enough.

Say clearly that this is a first impression and that you will check for existing solutions next.

## Search for existing solutions

Send the quick take and a one-line search plan to the user **before** running any search. Search terms describe the **idea only** — never names, personal details, or private content from the conversation.

Search, if you have web access:

1. **The CraftApps Library** — an app another maker built and shared, which the user could use, improve, or join. *The Library does not exist yet: skip this source and write "CraftApps Library: not available yet". Do not search the web for it. When it launches, its address will be listed here.*
2. **Open-source projects** on code hosts (GitHub, GitLab, Codeberg, and others) that do the same thing.
3. **Existing apps** in the stores for the user's devices, and built-in features of apps or systems they already use.

For each relevant result, note: name, what it does, cost or subscription, privacy (account needed? data in the cloud?), whether it is open source and maintained, and how well it fits.

If you have no web access, say so, rely on your knowledge, and mark the existing-solution list as unchecked.

## Options to offer

Present the honest options with trade-offs, and recommend one:

| Option | When it fits |
|---|---|
| **Use an existing app** | A good app fits and the user is happy with its cost and privacy |
| **Join a shared project** | An open project or CraftApps Library app is close; improving it helps everyone ("a people's project") |
| **Fork and adapt** | An open project is close but the user needs it to work differently |
| **Build their own** | Nothing fits, or they want ownership, privacy, no subscription, or to learn — always a valid choice |
| **Something smaller** | A Shortcut, script, or setting solves it |

## idea-check.md template

````markdown
---
craftapps_artifact: idea-check
schema_version: 1
produced_by: build-app
created: YYYY-MM-DD
status: draft            # approved once the user chooses a direction
source_artifacts: []     # e.g. [opportunity-brief.md] when coming from Discovery
experience: new | some | developer
user_devices: [<e.g. iPhone, Mac>]
web_search: done | unavailable
---

# Idea check: <name>

## The idea
<!-- In the user's words, then one sentence restating the problem. -->

## Quick take
- **Can build:** …
- **Can't / hard:** …
- **Needs:** …
- **Smaller alternative:** …

## Existing solutions

| Name | Type | What it does | Cost | Privacy | Fit |
|---|---|---|---|---|---|

<!-- Type: CraftApps Library app / open source / store app / built-in feature. "None found" is a valid result. -->

## Options
<!-- The relevant options from the table above, each with a one-line trade-off. -->

## Recommendation
<!-- One option and why, at the user's level. -->

## Decision
<!-- Filled in after the user chooses. -->
````
