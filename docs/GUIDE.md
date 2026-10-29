# How to use CraftApps

Step by step: what to say, what happens, and what you get from each skill. For installation, see the [README](../README.md#installation).

## Before you start

- **An AI agent** that can read files and run commands on your computer. Any capable LLM works, cloud or local.
- **The CraftApps skills**, installed as described in the README, or simply tell your agent: *"Read `skills/<skill-name>/SKILL.md` from CraftApps and follow it."*
- **Python 3**, only if you want `discover-app` to read your AI chat history (an export, or your Claude Code or Codex history). It runs the local cleanup step. Mac: install the Xcode Command Line Tools (`xcode-select --install`) or get it from [python.org](https://www.python.org). Windows: [python.org](https://www.python.org) or the Microsoft Store. Most Linux systems already have it. No Python? The interview works without it.

You can start with any skill. Each one writes plain Markdown files you can read and edit in a private `craftapps/` folder (by default, in the folder where you started the agent).

## Discover: find something worth building

### You say

> Find something useful I could build for myself. Use my Claude Code history.

or with files:

> Find something useful I could build for myself. Use the files in `~/craftapps-input/`.

or, with nothing to share:

> Interview me and find something useful I could build for myself.

### Choose what to share (optional)

- **AI coding tool history on this computer:** if you use Claude Code or Codex, there is nothing to export. Just say so; the cleanup script reads only that tool's history folder (`~/.claude/projects` or `~/.codex/sessions`).

Put any other material in one folder **outside any public repository**, for example `~/craftapps-input/`:

- **AI chat history:** ChatGPT (Settings → Data controls → Export data) or Claude (Settings → Privacy → Export data). Use the ZIP you receive as-is. For any other assistant, copy the conversations you want into a `.txt` file.
- **Notes:** to-do lists, journals, routines, a list of apps you use and what annoys you about them.
- **Projects:** folders of your own projects, if you want ideas around them.

### What happens

1. **Questions first.** The agent offers what it can use — your AI tools' history, chat exports, an interview, or your projects — and asks what to leave out (topics, people, dates) and where to save results. It works out your devices from what you share and asks you to confirm them with the report (in an interview, it simply asks).
   > **Your data:** nothing is read yet. The agent reads only the paths you name and never searches your computer for more.
2. **Local cleanup.** For chat history, the agent runs a script on your computer — no AI, no internet. It keeps only your own messages (for Claude Code or Codex history, it also drops tool output, commands, and sessions started by programs) and removes keys, passwords, emails, phone numbers, and any names you list.
   > **Your data:** the agent sees only counts, never your text. You can run the script yourself if you prefer, and the agent gives you the exact command if it isn't allowed to run it.
3. **You review.** Open `craftapps/cleaned/cleaned-input.md` (it starts with an index of conversations and sessions), delete anything you don't want an AI to see, and tell the agent to go ahead.
   > **Your data:** only after your approval does the agent read the cleaned file. With a cloud model, what it reads is processed by that model's provider. For maximum privacy, use a local model.
4. **The report.** On long files the agent tells you how far it has read as it goes. It finds repeated tasks, recurring problems, and ideas you never followed up on, scores each opportunity (how often it happens, what it costs you today, how hard it is to solve, how much it would help), and proposes the smallest solution that works — an app you already have, a saved prompt, an automation, or a small native app. Every suggestion cites its evidence and separates what was observed from what was assumed.
5. **You choose.** Pick the opportunities you like, or none.

### What you get

- `craftapps/discovery-report.md` — the opportunities and their evidence ([example](../skills/discover-app/examples/sample-report.md), synthetic data).
- `craftapps/apps/<name>/opportunity-brief.md` — a short brief for each opportunity you chose, ready for `build-app`.

> **Keep `craftapps/` private.** It contains personal information.

## Build: turn an idea into an app

### You say

> I want an app on my phone that reminds me which plants need water.

or hand over a brief from discovery:

> Build the app in `craftapps/apps/plant-reminder/opportunity-brief.md`.

### What happens

1. **Your level.** The agent asks whether you've built apps before, and which devices you use. If you're new, it uses plain language and does everything for you; if you're a developer, it keeps technical choices short. Say "explain more" or "skip the details" anytime.
2. **Idea check.** An honest first answer: what it can build, what isn't possible, what you'd need. Then it tells you what it will search for, and searches online for existing apps, open-source projects, and built-in features. You choose: use an existing app, improve a shared one, or build your own.
   > **Your data:** search terms describe the idea only, never you or your personal details.
3. **Plan.** A short plan you approve: what the first version does (and doesn't), which device it runs on, where your data stays, where your app's code will be kept on your computer, whether you want a private backup copy (for example in your cloud drive or a private repository), and anything you'll need to install.
4. **Build.** Small steps; the agent builds and runs the app after each one and tells you what it actually ran.
   > **Your data:** the app keeps your data on your device, with no tracking or analytics. The agent asks before installing anything or touching files outside the project folder.
5. **Verify.** The agent checks the app against the plan, including privacy, security, and accessibility, fixes what fails, and tells you what was not tested.
6. **You try it.** You accept it when it works for you. The agent explains how to run it day to day and where its data lives.

If your agent has general process skills installed, such as [Superpowers](https://github.com/obra/superpowers), `build-app` uses the matching ones (test-first development, systematic debugging, code review). Nothing requires them.

### What you get

- The app's source in its own folder, with `HOW-IT-WORKS.md` so you understand what you own and can change it.
- In `craftapps/apps/<name>/`: `idea-check.md`, `plan.md`, `build-report.md`, and `verification-report.md`.

## Share: give your app to others (optional)

### You say

> Share my app with my sister on Dropbox.

or:

> Put my app on GitHub so anyone can use it.

### What happens

1. **One question.** If you haven't said, the agent asks only: "Do you want to share your project publicly?" — publicly, only with certain people, or not now.
2. **Where.** It suggests a place that fits what you already use (your code host, Dropbox, Google Drive, iCloud Drive, a zip file), or asks where you usually share files.
3. **A clean copy.** It prepares what will be shared in a separate folder and checks it for secrets, personal data, and private notes. Your project's own files are not changed.
4. **You see exactly what will be shared.** Where, who can see it, the full file list, what was left out and why, and (for public shares) a license recommended in plain words. Nothing is shared until you say yes to that list.
   > **Your data:** nothing leaves your computer before this yes. The agent uses your own account and tools, never asks for passwords, and invites only people you name in the conversation.
5. **Share.** The agent shares it, or gives you step-by-step instructions if it can't.
6. **CraftApps Library (optional, public shares only).** The agent asks once whether you'd like to submit it, so others with the same problem can use it. If yes, it drafts an email for you to send from your own address to craft.apps@aigarden.uk. The library is planned; the maintainer reviews every submission before anything is listed.

### What you get

- Your app, shared where you chose.
- `craftapps/apps/<name>/share-record.md` — a private note of what was shared, where, and with whom. It is never shared.
