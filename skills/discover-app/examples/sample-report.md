---
craftapps_artifact: discovery-report
schema_version: 1
produced_by: discover-app
created: 2026-10-14
status: draft
sources:
  - path: craftapps/cleaned/cleaned-input.md
    kind: cleaned-export
    cleaned_locally: true
    coverage: all user messages, 10 conversations (5 ChatGPT, 5 Claude), plus notes.md and apps-i-use.md
    date_range: 2026-02-03..2026-09-30
excluded: []
user_devices: [iPhone, iPad, Mac]
---

<!-- SYNTHETIC EXAMPLE: reference output for the fixture in examples/discovery/synthetic-ios-developer/. Fictional person and apps. -->

# Discovery Report

## Summary

I read 10 AI conversations (February–September 2026), your notes, and your app list. Most of your repeated AI use is **release chores for your iOS apps**: writing and translating "What's New" text every release, sorting App Store reviews, and catching missing translations. You also spend about 20 minutes every Monday copying crash numbers by hand. The strongest recommendation is a small Mac automation for release notes using fastlane, which you already have installed. None of the four opportunities needs a new account, subscription, or server.

## At a glance

| ID | Opportunity | Frequency | Cost today | Complexity | Value | Evidence | Suggested solution |
|---|---|---|---|---|---|---|---|
| OPP-1 | Release notes + translations | Per release | High | S | High | Strong | Mac script + fastlane (rung 2) |
| OPP-2 | Missing-translation check | Per release | High | XS–S | High | Strong | Xcode build step on the Mac (rung 2) |
| OPP-3 | Review triage and replies | Occasional | Medium | S | Medium | Strong | Mac script + saved prompt (rung 2) |
| OPP-4 | Weekly crash tracking | Weekly | Medium | M | Medium | Strong | Scheduled Mac task (rung 2) |

## Scope and coverage

- Your raw exports were never opened. They were cleaned on your computer (your messages only; 3 secrets, 1 email, 1 phone number removed), and I read the cleaned file after you approved it.
- All of your messages in both exports were read. Assistant replies were removed by the cleanup, so they were not used.
- Notes and the app list are undated, so they support patterns but not frequency.
- Dates come from conversation timestamps. With 10 conversations, frequencies are rough.

## Opportunities

### OPP-1: Release notes and translations pipeline

- **Problem:** Every release you collect commits, ask an AI for friendly "What's New" text, ask for five translations, then paste six versions into App Store Connect one by one.
- **Evidence:** O1, O4, O7, O10 (four releases, 2.3–2.6, Observed); workflow in O12; friction in O18 and O20 (Observed).
  > "I do this every release and it's tedious, and I always forget which languages the app supports." — Release notes 2.5, 2026-07-08
  > "Then I'll paste each one into App Store Connect by hand, five times." — What's New 2.6, 2026-09-28
- **Frequency:** 4 times between 2026-02-03 and 2026-09-28, about every 11 weeks (Observed). Your notes say releases happen every 6–8 weeks; if so, some release notes were written elsewhere (Inferred).
- **Cost today:** High — "tedious", re-explained rules each time, six manual pastes per release (Observed).
- **Recommended solution:** Rung 2 — a Mac command you run when a release is ready. It collects commits since the last git tag, applies your standing rules (friendly, under 500 characters, skip refactors and dependency bumps), produces English plus translations for the languages the app actually supports, writes them into fastlane's metadata folders, and — after you review the text — uploads them with fastlane. Start today with rung 1: save your instructions as a reusable prompt.
- **Why this rung:** The steps are identical every time and need no interface beyond reviewing the text. An app would add nothing.
- **Alternatives considered:** Rung 1 alone (saved prompt) removes re-explaining but not the six manual pastes. Rung 3 (Mac app) is unnecessary.
- **Value:** High — every release, and it removes manual pasting and the "which languages?" mistake.
- **Complexity:** S — main risk: fastlane's upload step needs an App Store Connect API key to be set up.
- **Evidence strength:** Strong
- **Privacy:** Commit messages go to whichever AI generates the text, as they do today. The API key must be stored in the macOS Keychain or a file outside the repository, never in source code. Runs on your Mac.
- **Assumptions to confirm:** That you want to keep reviewing the text before upload (Assumed). Which AI you want the command to use, or whether you prefer to keep pasting into a chat (Assumed).

### OPP-2: Missing-translation check before archiving

- **Problem:** Releases ship with untranslated strings, and users notice before you do.
- **Evidence:** O11 (shipped with missing Japanese strings, Observed); checklist step "manual, I often forget" in O12; idea noted twice in O14 (Observed).
  > "Again I shipped with missing translations in Localizable.xcstrings." — Missing Japanese strings, 2026-09-30
- **Frequency:** One shipped incident in the input (Observed); "Again" and "I often forget" indicate earlier ones (Inferred). The check itself is due every release.
- **Cost today:** High — a missed check reaches users as untranslated text (Observed: a user emailed about it).
- **Recommended solution:** Rung 2 — a small check on the Mac that reads your string catalogs and stops the archive (or warns loudly) if any key lacks a finished translation for a supported language. It runs automatically as an Xcode build step for Release builds, so there is nothing to remember.
- **Why this rung:** Xcode's String Catalog editor shows translation progress, but looking at it is exactly the manual step being forgotten. An automatic check fixes that; an app would not.
- **Alternatives considered:** A checklist reminder (rung 0) has already failed. Combining this check into OPP-1's release command is a good option.
- **Value:** High — prevents visible bugs for users in five languages.
- **Complexity:** XS–S — string catalogs are JSON files; the risk is only edge cases such as plural variations.
- **Evidence strength:** Strong
- **Privacy:** Reads only your project files, locally. No network.
- **Assumptions to confirm:** Whether a warning or a hard stop is preferred (Assumed).

### OPP-3: App Store review triage and replies

- **Problem:** You copy reviews out of App Store Connect app by app, ask an AI to sort them and spot repeated bugs, then paste replies back.
- **Evidence:** O2, O8 (two triage sessions, Observed); O3 and O18 (copying friction, Observed); O15 (idea, Observed); O20 (re-explaining instructions).
  > "Copy-pasting these from App Store Connect takes forever." — Sort reviews and draft replies, 2026-03-17
- **Frequency:** At least twice (2026-03-17, 2026-08-12) (Observed). "the last two weeks of App Store reviews" suggests you intend a fortnightly routine (Inferred).
- **Cost today:** Medium — "takes forever" to copy reviews, across several apps (Observed).
- **Recommended solution:** Rung 2 — a Mac command that fetches new reviews for all three apps through the App Store Connect API and writes one grouped Markdown file per run, ready to paste into your saved triage prompt. You still post replies yourself. Upgrade to rung 3 (a small Mac app that shows reviews across apps, drafts replies, and posts the ones you approve) only if pasting replies remains the bottleneck.
- **Why this rung:** Fetching is the fixed, tedious part. Deciding replies needs you, and a chat already handles drafting.
- **Alternatives considered:** Rung 1 (saved prompt) alone; rung 3 Mac app (above).
- **Value:** Medium — saves copying time and makes repeated bugs visible across apps.
- **Complexity:** S for rung 2, M for rung 3 — main risk: API authentication (O3 shows an earlier attempt failed with a 401 error).
- **Evidence strength:** Strong
- **Privacy:** Reviews are public. Requires an App Store Connect API key stored in the Keychain. **An API key appears in your ChatGPT export (O3); see Privacy notes.**
- **Assumptions to confirm:** That replies should never be posted without your approval (Assumed).

### OPP-4: Automatic weekly crash tracking

- **Problem:** Every Monday you copy crash and session counts for three apps from Xcode Organizer into Numbers. When you skip it, your chart has gaps.
- **Evidence:** O6, O13, O19 (Observed).
  > "Takes ~20 minutes, boring, sometimes I skip it and then the chart has gaps" — notes.md
- **Frequency:** Weekly (Observed, by your description). About 17 hours a year (Inferred: 20 min × 52 weeks).
- **Cost today:** Medium — about 20 minutes, "boring", skipped weeks leave gaps (Observed).
- **Recommended solution:** Rung 2 — a scheduled Mac task that fetches crash and session numbers for your three apps every Monday and appends them to a file your Numbers sheet reads. A small Mac widget or menu-bar app (rung 3) is possible later if you want the trend at a glance.
- **Why this rung:** The work is collecting numbers on a schedule; your sheet already does the analysis.
- **Alternatives considered:** A third-party crash-reporting SDK — rejected: it adds a dependency to all three apps and sends crash data to another company.
- **Value:** Medium — weekly time saved and no gaps in the data.
- **Complexity:** M — main risk: it is unconfirmed that the same crash numbers you see in Organizer are available programmatically (Assumed; must be verified first).
- **Evidence strength:** Strong
- **Privacy:** Aggregate app data only; requires the same App Store Connect API key as OPP-3, if that route works.
- **Assumptions to confirm:** That an Apple data source matches the Organizer numbers (Assumed).

## Weak signals

| Signal | Observations | Why not an opportunity |
|---|---|---|
| Home workout plan | O5 | Single request, answered fully by the chat; no recurring need. |
| Recipe scaler app | O16 | One line in an ideas list, no other evidence; fails the generic-idea test. |
| Client email about a delay | O9 | One-off writing task. |

## Observations

| ID | Date | Source | Type | Excerpt or summary |
|---|---|---|---|---|
| O1 | 2026-02-03 | ChatGPT · What's New text for 2.3 | repeated task | Commits → What's New, "under 500 characters", translated into 5 languages |
| O2 | 2026-03-17 | ChatGPT · Sort reviews and draft replies | repeated task | "Sort them into bugs, feature requests and praise" |
| O3 | 2026-03-17 | ChatGPT · Sort reviews and draft replies | tool friction | "Copy-pasting these from App Store Connect takes forever." API attempt failed. [REDACTED: API key] |
| O4 | 2026-04-21 | ChatGPT · Release notes 2.4 + translations | repeated task | "Same as last time" |
| O5 | 2026-05-09 | ChatGPT · Beginner workout plan | other | One-off request for a workout plan |
| O6 | 2026-06-01 | ChatGPT · Numbers formula for crash trend | manual workflow | "I copy crash counts and sessions for my three apps from the Xcode Organizer into a Numbers sheet every week." |
| O7 | 2026-07-08 | Claude · Release notes 2.5 | repeated task | "I do this every release and it's tedious" |
| O8 | 2026-08-12 | Claude · Review replies August | repeated task | Reviews for two apps; "tell me which bugs show up more than once" |
| O9 | 2026-08-20 | Claude · Email about delayed project | other | Email to [client] about a delivery delay |
| O10 | 2026-09-28 | Claude · What's New 2.6 | repeated task | "You know the drill" |
| O11 | 2026-09-30 | Claude · Missing Japanese strings | recurring problem / abandoned idea | "I really should build something that checks the string catalog for untranslated keys before I archive." |
| O12 | undated | notes.md · Release checklist | manual workflow | Steps 2–5: AI release notes, translations, 6 manual pastes, manual catalog check |
| O13 | undated | notes.md · Monday routine | manual workflow | "Takes ~20 minutes, boring" |
| O14 | undated | notes.md · Ideas | abandoned idea | "Tool that checks for missing localizations before archiving — I wrote this down in March too" |
| O15 | undated | notes.md · Ideas | unmet need | "Reply to reviews faster, maybe pull them automatically" |
| O16 | undated | notes.md · Ideas | other | "Recipe scaler app?" |
| O17 | undated | apps-i-use.md | context | fastlane used "Only for screenshots" |
| O18 | undated | apps-i-use.md | tool friction | "Pasting localized What's New text one locale at a time; reading reviews app by app" |
| O19 | undated | apps-i-use.md | tool friction | "Organizer crash data can't be exported the way I want" |
| O20 | undated | apps-i-use.md | tool friction | "Re-explaining the same instructions every time" |

## Privacy notes

- **Your ChatGPT export contains what looks like an App Store Connect private key, key ID, and issuer ID** (conversation "Sort reviews and draft replies", 2026-03-17). The local cleanup removed them before I read anything. If that key is still active, revoke it in App Store Connect and create a new one.
- A client's email address and phone number were removed by the cleanup. Their name was still in the cleaned file (names are not detected automatically); it is replaced with [client] here. Next time, pass names with `--redact-term`.
- This report contains personal information about your work. Keep it private and do not commit it to a public repository.

## Next step

Which opportunities would you like to explore? Reply with IDs (e.g. "OPP-1 and OPP-2"), "none", or questions. OPP-1 and OPP-2 fit well together as a single "release prep" command. Chosen opportunities get an opportunity brief that a requirements step or a coding agent can build on.
