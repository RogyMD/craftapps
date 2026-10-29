---
name: share-app
description: Use when a person wants to share an app or project they built — "share my app", "send it to my sister", "put it on Dropbox / GitHub / GitLab", "make it public", "submit it to the CraftApps library / CraftApps Library". Part of CraftApps.
---

# Share App

Help a person share what they built — with specific people or publicly, wherever they already share things — **without ever leaking a secret or a private detail.**

**Core rule: nothing leaves the computer until the person has seen exactly what will be shared, where, and who can see it, and said yes to that.** "Just do it" before they have seen the list is not a yes to the list. Violating the letter of this rule is violating its spirit.

## When not to use

- Releasing to app stores → not covered by CraftApps; point the person to the store's official guide.
- The app isn't finished or verified → finish with `build-app` first, or say clearly that it's unfinished.

## Process

### 1. One question first

If the person has **not** already said how they want to share, ask only: **"Do you want to share your project publicly?"** (adapt wording to their experience — see `build-app`'s experience-levels guide). Answers: *publicly*, *only with certain people*, or *not now*.

If they **already** said ("put it on Dropbox for my sister", "submit it to the library"), don't ask again — go to step 2 and confirm it at the checkpoint.

### 2. Where — from context, not from a list

Offer only places that fit what you already know. Look **only** at the project folder and the conversation:

- The project has a git remote → offer that host ("Share it on your GitLab repo?").
- They mentioned Dropbox, Google Drive, iCloud Drive, OneDrive, a website, a USB stick → offer that.
- Nothing known → ask "Where do you usually share files?" and suggest one simple option for their level (e.g. a zip file).

Never search their disk, accounts, or apps to find services. People to share with come **only** from names and addresses the user gives you in this conversation — never from files in the project.

### 3. Prepare a clean copy

Build what will be shared in a new folder **outside the project folder** (for example in the system's temporary folder), following [references/safe-share-checklist.md](references/safe-share-checklist.md). Never add, change, or delete the project's own files. (The only file you write is the share record in step 7, inside the private `craftapps/` workspace, which is never shared.)

### 4. Show and ask (checkpoint)

Send one message containing, in this order:

1. **Where** and **who can see it** ("public — anyone with the link", or "only Lena").
2. **Exactly what will be shared:** the full file list.
3. **What was left out and why** (secrets, personal notes, history).
4. **License** (for public sharing): recommend one in plain words; MIT if they have no preference.
5. The question: "Share exactly this? (yes / change something)".

If they are in a hurry, keep it to these five lines — but still send it and wait.

### 5. Share

Use the person's own account and tools. Never ask for passwords. If you can't do the upload yourself (no CLI, no access), give them step-by-step instructions to do it, at their level. Send invites only to people they named.

### 6. CraftApps Library (optional, public shares only)

Ask once: "Would you like to submit it to the CraftApps library, so others with the same problem can use it?" If yes, **draft** the email in [references/library-submission.md](references/library-submission.md) for them to send from their own email. You never send it, and you never fill in their address.

### 7. Record

Write `craftapps/apps/<slug>/share-record.md` (template in the checklist reference), in the user's existing `craftapps/` workspace. It stays private with the user's other `craftapps/` files and is always excluded from sharing.

## Process skills (optional)

If your agent has general process skills installed (for example Superpowers), use `verification-before-completion` before the checkpoint: run the scans in the checklist and read their output before telling the person the copy is clean. This skill's checkpoint and rules always take precedence; never name process skills to newcomers.

## Red flags — stop and go back to step 4

| Thought | Reality |
|---|---|
| "They said just do it / I trust you" | That was before they saw the list. Show it; one word from them is enough. |
| "I removed the secrets, so it's safe to skip the confirmation" | Your cleanup may have missed something only they would recognize. |
| "The sister's email is right there in the notes" | Private files are not a contact book. Ask them who to share with. |
| "I redacted the name, so the planning notes are fine" | `craftapps/` notes are private. Leave them out entirely. |
| "Sending the submission email myself is faster" | Draft it; they send it from their own address. |
| "It's going to a library, so it's obviously open source" | Public sharing needs a license they chose. |
| "No need to reply, I'll carry on" | Always wait at the checkpoint. |
