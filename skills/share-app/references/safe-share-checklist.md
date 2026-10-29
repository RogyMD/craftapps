# Safe-share checklist

Prepare the shared copy in a new folder **outside the project folder** (for example under the system's temporary folder); never add, change, or delete anything inside the original project.

## Always leave out

| What | Why |
|---|---|
| `craftapps/` folder and any CraftApps artifacts | Private planning notes about the person's life |
| Personal notes, to-do files, journals, contacts | Private |
| Secrets: API keys, tokens, passwords, `.env`, `*.p8`, `*.p12`, `*.pem`, keystores, provisioning profiles, credential plists/JSON | Can be abused; often costly to rotate |
| `.git` history, unless scanned clean (see below) | History keeps files that were deleted later |
| Build output and dependency folders (`build/`, `DerivedData/`, `.build/`, `node_modules/`, `Pods/`) | Large, machine-specific |
| OS and editor files (`.DS_Store`, `.idea/`, `xcuserdata/`) | Noise; can contain local paths and user names |

If the app needs a secret to run, replace it with a placeholder file (`Config.example.plist`, `.env.example`) and explain in the README how to add one's own.

## Scan the clean copy

Search the prepared folder (not just file names) for anything that looks private:

```sh
grep -rniE 'api[_-]?key|secret|token|password|passwd|BEGIN [A-Z ]*PRIVATE KEY|sk-[A-Za-z0-9]{16}|gh[pousr]_|AKIA[0-9A-Z]{16}' <clean-copy>
grep -rnE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' <clean-copy>
```

Read every match. Also check for: real names, addresses, phone numbers, door codes, locations, photos of people, and the person's own name or username in file headers or paths. When unsure, ask the person.

Commits carry the author name and email from the person's git settings. Before pushing a public history, tell them which name and email will be visible, so they can change it if they prefer.

## Git history

Sharing to a code host shares the whole history. Check it:

```sh
git -C <project> log --all --stat          # which files were ever committed
git -C <project> log --all -p | grep -niE 'api[_-]?key|secret|token|password|BEGIN .*PRIVATE KEY'
```

If history contains anything private, share a **fresh history** instead: a new repository initialized from the clean copy. Tell the person why, in plain words. If a real secret was ever pushed anywhere public, tell them to revoke it — removing it is not enough.

## For other people to use it

Make sure the clean copy has:

- A `README.md` for strangers: what it does, which devices, how to build or install it, and that it was made with CraftApps.
- A `LICENSE` file for public sharing (the license the person chose).
- Honest status: "works on my iPhone; not tested elsewhere" is fine.

## share-record.md template

````markdown
---
craftapps_artifact: share-record
schema_version: 1
produced_by: share-app
created: YYYY-MM-DD
status: approved          # only after the person said yes to this exact list
source_artifacts: [verification-report.md]   # if available
visibility: public | people
where: <e.g. "GitLab: gitlab.com/…", "Dropbox shared link", "zip file sent by the person">
license: <e.g. MIT, or "none (private share)">
library_submission: drafted | not-wanted
---

# Shared: <app name>

## Shared files
<!-- The exact list the person approved. -->

## Left out
<!-- And why. -->

## Who can see it
<!-- "Anyone with the link" / named people (as given by the person). -->

## Follow-ups
<!-- e.g. "Revoke the old weather API key", "Send the library email". -->
````
