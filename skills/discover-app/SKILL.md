---
name: discover-app
description: Use when a person wants to find software, automations, or apps they could build for themselves based on their own life and work — AI conversation exports, notes, workflows, existing projects, or simply an interview about their routines. Triggers include "what could I build for myself", "find something useful to build", "look at my ChatGPT, Claude, Claude Code, or Codex history", "analyze my workflows for automation opportunities", or "what do I keep asking AI to do". Part of CraftApps.
---

# Discover App

Find personal software opportunities **grounded in evidence** about the user's real life and work. Recommend the smallest solution that works — often an automation or an existing tool, sometimes a small native app. The user chooses what to pursue.

**Security first.** Never open a raw conversation export or AI tool session log, not even to peek at its format. They are cleaned locally by [scripts/prepare_input.py](scripts/prepare_input.py) (no AI, no network), the user reviews the result, and only the approved cleaned file is read. Nothing is ever sent anywhere else.

**No evidence, no opportunity.** Every opportunity cites specific observations. Never invent quotes, counts, dates, or patterns.

**The goal is not many ideas.** It is finding one problem worth solving that the user had not recognized.

## When not to use

- The user already has an idea → use `build-app`.
- The user wants generic brainstorming → offer it, but explain this skill needs their material or an interview.

## Discovery modes

Use one or combine several. The skill works even with no files at all.

| Mode | Input | Details |
|---|---|---|
| **Conversation analysis** | The history AI coding tools keep on this computer (Claude Code, Codex) or AI chat exports (any assistant; see supported formats) — **cleaned locally and approved by the user first** | [references/input-formats.md](references/input-formats.md) |
| **Workflow interview** | The user's answers to questions about routines, apps, and frustrations | [references/interview-guide.md](references/interview-guide.md) |
| **Project analysis** | Folders the user points to: projects, notes, scripts, existing apps | [references/input-formats.md](references/input-formats.md#projects-and-existing-apps) |

If the user has nothing to share, start with the interview.

## Outputs

1. `craftapps/discovery-report.md` — template: [references/report-template.md](references/report-template.md)
2. After the user chooses: `craftapps/apps/<slug>/opportunity-brief.md` per chosen opportunity — template: [references/opportunity-brief-template.md](references/opportunity-brief-template.md)

Example of a finished report: [examples/sample-report.md](examples/sample-report.md).

**Keep `craftapps/` out of git — before the first file is written.** It holds private notes about the person. If the folder you will write in is inside a git repository (`git rev-parse --show-toplevel` succeeds there):

1. Run `git check-ignore -q craftapps/`. If it is already ignored, go on.
2. If not, append the line `craftapps/` to the repository's local exclude file (its path is printed by `git rev-parse --git-path info/exclude`). That file is never committed, so the person's own `.gitignore` and project stay untouched. Edit `.gitignore` only if the person asks.
3. Run `git check-ignore -q craftapps/` again to confirm. If you cannot make it ignored, ask the person for a folder outside the repository and write there.
4. Tell the person in one plain sentence where their private notes are and that they are kept out of their project's history.

## Process

### 1. Agree on scope and explain privacy (before reading anything)

Ask, in one message, and wait for answers:

- **What to use.** Offer all of these as one short list, in this order — also when the person asked only for an interview, because their history often shows what they would not think to mention:
  1. **The history their AI tools keep on this computer** — Claude Code (`~/.claude/projects`) and Codex (`~/.codex/sessions`). Nothing to export. Name both; do not check whether the folders exist before the person says yes.
  2. AI chat exports (ChatGPT, Claude, or copied text from any assistant).
  3. An interview about their routines (no files needed).
  4. Project folders or notes they name.

  Read **only** what they choose. Never search the disk, browser, apps, or accounts for more.
- Anything to exclude (topics, people, date ranges, projects).
- Where to write output (default: `./craftapps/`).
- Optional: their role and whether they can code.

Do not ask which devices they use here: with material, step 7 infers them; in an interview, the interview guide asks.

In the same message, state plainly:

> I will not open your raw chat history or export. A script runs on your computer — no AI, no internet — to keep only your own messages and remove keys, passwords, emails, and phone numbers. You then read the cleaned file and delete anything you don't want shared. **Only after you approve it do I read it — and because I am an AI model, what I read is processed by my model provider.** Names of people are not removed automatically; tell me any names or words to remove, and topics to drop. The report I write will contain personal information — keep it private.

If the user already answered these, do not ask again.

### 2. Gather material

- **AI tool history or conversation exports:** run the cleanup locally (details in [references/input-formats.md](references/input-formats.md)), passing the user's names/terms to redact and topics to exclude:
  - History: `python3 -I <skill-dir>/scripts/prepare_input.py --from claude-code --out craftapps/cleaned --redact-term "<name>" --exclude "<topic>"` (`--from codex` for Codex; both may be given). It reads only that tool's history folder. Leave out `--redact-term` and `--exclude` only when the person named nothing to remove.
  - Export: `python3 -I <skill-dir>/scripts/prepare_input.py <export.zip or folder> --out craftapps/cleaned --redact-term "<name>" --exclude "<topic>"`

  The script prints only counts. **If you are not allowed to run it** (your permissions or sandbox refuse), give the person the exact one-line command to run themselves and wait. Never try another way to read the history or export.
- **Approval:** ask the person to open `craftapps/cleaned/cleaned-input.md`, delete anything they like, and tell you to go ahead. Any clear yes counts ("yes", "go", "go ahead", "looks good", "approved") — never insist on a particular word. If the reply is unclear ("hmm, there's a lot in there"), do not read; ask once whether to go ahead or what to remove, and offer to narrow it with `--since` or `--exclude`. **Never read it before a yes.**
- **Notes and other text files:** pass them through the same script, or ask the user to confirm they are safe to read as-is.
- **Projects:** read only folders the user named, following the skip list in the input-formats reference.
- **Large inputs:** reading a long file takes minutes. Before you start, say roughly how many parts you will read. Read in parts of about 1,000 lines, and after each part send the person one line, for example "Read 3 of 8 parts — 2 patterns so far." If the file is too large to read fully, choose a sampling plan and say what will and will not be covered.
- **Interview:** follow the interview guide. A few questions at a time; follow up on specifics.

### 3. Extract observations

Record atomic observations: one thing the user did, asked for, complained about, or wished for. Each gets an ID (`O1`, `O2`, …), a source reference (file and conversation title, project path, or "interview"), date if known, a type, and a short verbatim excerpt.

Types: **repeated task** · **recurring problem** · **format conversion** · **manual workflow** · **tool friction** · **unmet need** · **abandoned idea**.

Focus on what the *user* asked for and did. Assistant replies are context, not evidence of a need.

### 4. Group into patterns

Cluster observations by the **underlying job**, not surface wording ("turn commit log into release notes" and "write What's New from these changes" are one pattern). For each pattern record: observation IDs, number of distinct sources, first and last date, and frequency **only if dates or the user's own statements support it**.

### 5. Propose solutions with the solution ladder

For each pattern, climb only as high as needed:

| Rung | Solution | Choose when |
|---|---|---|
| 0 | **Use what exists** — a feature of a tool they already have | An existing tool already does it well |
| 1 | **Saved prompt or template** | The AI result is fine; only re-explaining is costly |
| 2 | **Automation** — script, Shortcut, scheduled task, build step | Steps are fixed and no UI is needed |
| 3 | **Small native app** for the user's devices | Needs persistent data, a UI, ongoing interaction, or device capabilities |
| 4 | **Larger native app** | Rarely. Only with strong evidence and explicit user interest |

State why lower rungs are insufficient whenever you recommend rung 3 or 4. Name the target device (e.g. "Mac app", "Android app") based on where the problem happens and what the user owns. Do not propose websites or hosted services. Prefer solutions that need no new accounts, subscriptions, servers, or third-party dependencies; if one would be required, say so under Complexity and Privacy. Leave framework and technology choices to the architecture stage.

### 6. Score each opportunity

Rate **frequency**, **cost today** (time and frustration per occurrence), **complexity**, **value**, and **evidence strength**, plus privacy notes, using [references/assessment-rules.md](references/assessment-rules.md). Label every claim **Observed** (in the input or the user's own words), **Inferred** (reasoned from observations), or **Assumed** (must be confirmed).

Apply the **generic-idea test**: if this idea could be suggested to anyone without knowing this person (a to-do app, a habit tracker), drop it unless the evidence is specific to them. Single-mention and weak items go in *Weak signals*, not *Opportunities*.

### 7. Write the report, then let the user choose (checkpoint)

Write the report using the template, starting with the at-a-glance table. Redact secrets and third-party personal details (see assessment rules). Summarize the top opportunities in a few lines and ask which, if any, to explore. "None" is a valid answer. Stop here until the user replies.

**Devices.** If the person did not state their devices, take them from the material: list them in `user_devices` marked as inferred, with the evidence in *Scope and coverage*, and in the same checkpoint message ask them to confirm or correct the list. Ask about devices directly only when nothing in the material shows them.

### 8. Write briefs for chosen opportunities

For each chosen opportunity, write an opportunity brief with `status: draft`. A brief carries **only** what the next stage needs — no raw conversation content beyond short redacted excerpts. Ask the user to review it; set `status: approved` only on their explicit approval. Then explain the next step: building it with `build-app`, which starts by checking for existing apps.

## Process skills (optional)

If your agent has general process skills installed (for example Superpowers), use `verification-before-completion` before showing the report: check that every observation and score traces to quoted evidence in the approved input. Process skills never change what you may read — the raw-export rule above still applies — and are never named to newcomers.

## Boundaries

- Never open raw conversation exports or session logs. Only the user-approved cleaned file.
- No network requests with user data. No uploading, no web search of personal content, no sharing with other services or people.
- Never run code from the user's projects; read only.
- Never claim complete coverage when the input was sampled; state coverage in the report.
- Never decide for the user. Recommend; they choose.
- Fewer, well-evidenced opportunities beat a long list. Three to seven is typical; zero is acceptable.

## Common mistakes

| Mistake | Fix |
|---|---|
| Asking for a chat export when the person's AI tools keep history on this computer | Offer Claude Code and Codex history by name in the first message |
| Waiting for the exact word "approved" | Any clear yes is approval; ask once only if the reply is unclear |
| Minutes of silence while reading a large file | One progress line after each part |
| Asking about devices the material already shows | Infer them, mark them inferred, confirm at the checkpoint |
| Idea list that fits anyone | Apply the generic-idea test; cite observation IDs |
| "You often…" with no count | Count, or say the frequency is unknown |
| Paraphrase presented as a quote | Quotes are verbatim and short; otherwise label as paraphrase |
| Recommending an app for a fixed sequence of steps | Use rung 2 (automation) |
| Missing an existing tool the user already has | Check their app list, projects, and conversations for rung 0 first |
| Proposing a web app, or a platform the user doesn't use | Native solution on the user's own devices |
| Interview turned into a questionnaire dump | Few questions at a time; ask for the last concrete example |
| Copying an API key or a client's email into the report | Redact: `[REDACTED: API key]`, `[client]` |
| Peeking at the raw export "just to check the format" | Run the script; it reports field names for unknown formats, never content |
| Reading the cleaned file before the user approves it | Wait for explicit approval |
