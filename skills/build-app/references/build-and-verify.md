# Phases 3–4 — Build and verify

## Before building

- Create the project in the folder the approved plan names, set up as its own git repository.
- Set up the backup the plan names, and nothing else: a **private** repository on the person's own code host account (check it is private before the first push), or a folder in their cloud drive for zipped copies. No backup in the plan → nothing leaves the computer.
- Check required tools are installed. Install nothing without asking; guide at the user's level.
- Never put secrets in source code or commit them. Add a `.gitignore` suited to the platform.

## Build loop

For each build step in the approved plan:

1. Implement the smallest piece that can run.
2. Build it and run it (simulator, emulator, or device). Run tests if they exist; add tests for logic that can break silently (calculations, data parsing, date handling).
3. Fix errors before moving on. If a step is blocked (missing tool, account, permission), stop and explain what is needed.
4. Tell the user what now works, at their level. For newcomers, show how to see it themselves.
5. Commit with a clear message if the project uses git. Push only to the private backup the plan names; with a cloud-drive backup, put a fresh zipped copy (without build folders) there at the end of each working session.

If the plan turns out to be wrong (an API doesn't exist, a limit appears), stop and propose a plan change. Don't silently build something different.

## HOW-IT-WORKS.md (in the app folder)

Write it for the owner, at their level:

- What the app does, in a few sentences.
- Where its data lives and how to back it up or delete it.
- How to run it (and, on Apple devices, how to re-sign it when a free signing certificate expires).
- How to change common things — for newcomers, phrased as requests they can give an AI agent ("Ask your agent to change the reminder time in Settings").
- For **some** and **developer** levels: a file map and the main parts of the code.

## build-report.md template

````markdown
---
craftapps_artifact: build-report
schema_version: 1
produced_by: build-app
created: YYYY-MM-DD
status: draft
source_artifacts: [plan.md]
app_path: <path to the app's source folder>
---

# Build report: <app name>

## Built and run
<!-- Each plan item: done / partly / not done, and how it was run (simulator, device, tests). -->

## Not done or not tested
<!-- Be specific. -->

## Deviations from the plan
<!-- What changed and why, with the user's agreement. -->

## How to run
<!-- Steps at the user's level. -->
````

## Verification

Verify from a fresh look at the code and the plan — not from memory of having written it. Use a fresh session or a separate reviewer if available.

Checklist:

- [ ] Every "first version" item in the plan works, checked by running the app.
- [ ] The app builds from a clean state and runs on the target devices (or their simulators).
- [ ] Errors are handled: empty states, invalid input, denied permissions, no network (if used).
- [ ] **Privacy and security:** no secrets in code or git history; data stored only where the plan says; no analytics, tracking, or unexpected network calls; only the permissions the plan lists.
- [ ] **Dependencies:** only those justified in the plan.
- [ ] **Backup:** as the plan says — the private copy is up to date and still private, or "no backup" as agreed.
- [ ] **Accessibility:** works with large text and the screen reader; labels on icon buttons; adequate contrast.
- [ ] **Simplicity:** no unused code, features, or abstractions beyond the plan.
- [ ] `HOW-IT-WORKS.md` exists and matches the app.
- [ ] Tests exist for logic that can break silently, and they pass.

Return to the build loop for any failure, then re-verify.

## verification-report.md template

````markdown
---
craftapps_artifact: verification-report
schema_version: 1
produced_by: build-app
created: YYYY-MM-DD
status: draft            # approved when the user accepts the app
source_artifacts: [plan.md, build-report.md]
---

# Verification: <app name>

## Result
<!-- Ready / ready with known issues / not ready. -->

## Checklist
<!-- Each item: pass / fail / not checked, with a one-line note. -->

## Known issues
<!-- With severity and whether the user accepted them. -->
````

## After acceptance

Explain at the user's level: how to run it day to day, where data lives, where the project's code is and where its backup is (if any), and that sharing is optional — on a code host, a file-sharing service such as Dropbox, as a zip file, or in the CraftApps Library. App-store release is not covered by CraftApps. Never share or publish without explicit approval.
