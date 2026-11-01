# CraftApps

**Craft your own apps.**

CraftApps is a set of skills for your AI agent that helps anyone — developer or not — find, build, and share small apps they own.

## Table of Contents

- [The goal](#the-goal)
- [How it works](#how-it-works)
- [Installation](#installation)
- [The basic workflow](#the-basic-workflow)
- [Your privacy](#your-privacy)
- [What's inside](#whats-inside)
- [Philosophy](#philosophy)
- [Community](#community)
- [Contributing](#contributing)
- [Updating](#updating)
- [License](#license)

## The goal

- **Independence.** Small apps you own, that keep working without a subscription, an account, a server — or an AI.
- **Fewer tokens.** If you ask an AI to do the same thing every week, an app can do it for free, forever. And an app built once and shared doesn't need to be built again.
- **Your data stays yours.** On your devices, under your control, never handed to a company to make a simple thing work.

## How it works

It starts when you tell your agent "find me something useful to build" or "I have an idea for an app." It doesn't jump into code. First it asks whether you've built anything before, and talks to you at that level — plain words and every step done for you, or short technical choices if you're a developer.

If you want ideas, it looks only at what you choose to share — your AI chats, your routines, your projects — and finds the problems you keep hitting. If you have an idea, it checks whether an app already does it and tells you honestly what's possible.

Then it plans with you, builds in small steps, and checks each one. The result is a native app for the devices you already use (or a Shortcut or script, when that's enough), with no subscription, no account, and your data on your device. You approve at every turn, and nothing you share leaves your computer except to the AI model you chose.

It works with any capable LLM, cloud or local, and any agent that can read files and run commands. Want to know why I made it? Read [docs/VISION.md](docs/VISION.md).

## Installation

### Claude Code

```
/plugin marketplace add RogyMD/craftapps
/plugin install craftapps@craftapps
```

### Codex

This repository is also a Codex plugin marketplace (`.agents/plugins/marketplace.json`). Add it from Codex's plugin settings.

### Any other agent

Download or clone this repository, then either copy or link the folders in `skills/` into your agent's skills folder (many agents that support the open [Agent Skills](https://agentskills.io) format use `~/.agents/skills/`), or tell your agent:

> Read `skills/discover-app/SKILL.md` from CraftApps and follow it.

Step-by-step instructions for each skill: [docs/GUIDE.md](docs/GUIDE.md).

## The basic workflow

1. **discover-app** — Activates when you ask for ideas ("Find me something useful to build"). Looks at your AI conversations (chat exports, or the history Claude Code and Codex keep on your computer), an interview about your routines, or your projects — only what you choose to share — and finds problems worth solving. Every suggestion cites its evidence and proposes the smallest fix that works: a tool you already have, a saved prompt, an automation, or a small app. You choose what to explore.

2. **build-app** — Activates when you have an idea ("I want an app that…"). Gives you an honest first answer, searches online for apps that already do it, then plans, builds, and verifies the app with you, step by step, at your level. Writes `HOW-IT-WORKS.md` so you understand what you own.

3. **share-app** — Activates when you want to share ("Share my app with my sister", "Put it on GitHub"). Shares wherever you like — a code host, Dropbox, Google Drive, iCloud Drive, or a zip file — after checking for secrets and personal data and showing you exactly what will be shared.

You can start at any step. Skills pass work to each other as plain Markdown files you can read and edit, and **you decide at four checkpoints:** what to build, the plan, whether the app is done, and anything made public.

## Your privacy

- **Your raw chats never go to an AI.** A script cleans them on your computer — no AI, no internet — keeping only your own messages and removing keys, passwords, emails, and phone numbers. For your AI coding tools' history, it reads only that tool's folder and drops tool output, commands, and file contents.
- **You approve what's read.** You review the cleaned file and delete anything you like before the agent reads it.
- **Nothing is sent anywhere.** The skills don't upload, share, or call any service with your data. Web searches describe the idea, never you.
- **No telemetry.** CraftApps doesn't know you use it.
- **Private notes stay private.** Reports and plans live in a `craftapps/` folder that is kept out of git, even inside your own projects.
- **For maximum privacy, use a local model.** With a cloud model, what the agent reads is processed by that model's provider.

## What's inside

**For everyone**

- **discover-app** — find personal software worth building, from your own material
- **build-app** — check, plan, build, and verify an app, at your level
- **share-app** — share safely, anywhere you choose

**For the library maintainer**

- **curate-app** — review submissions to the CraftApps Library as untrusted code (never runs them) and prepare entries the maintainer approves. The CraftApps Library, a free list of apps people made with CraftApps, is planned; submissions by email are already welcome.

**Helpers**

- **prepare_input.py** — the local cleanup script for chat exports and AI tool history (Python standard library only, no network)

All four skills are early. See [docs/ROADMAP.md](docs/ROADMAP.md) for what has been tested.

## Philosophy

- **Security first** — above everything else. Your data stays with you.
- **Own your software** — your apps, your code, your data, and an understanding of how they work.
- **Small is beautiful** — sometimes the best answer is a Shortcut or a script, not an app.
- **Native, few dependencies** — built for your devices with what they already provide.
- **You decide** — AI suggests; you approve.

More in [docs/VISION.md](docs/VISION.md).

## Community

CraftApps is a fruit grown by Igor Bidiniuc. Check out [his garden](https://aigarden.uk/) for more fruits.

- **Issues:** bugs, ideas, and questions at https://github.com/RogyMD/craftapps/issues

## Contributing

Contributions are welcome — including from people who don't code. The most valuable ones:

- **Test cases** — synthetic personas with realistic habits, and what a good run should find.
- **Feedback** — where a skill found something genuinely useful, and where it was generic or confusing.
- **Skill improvements** — clearer instructions, better templates.

To contribute:

1. Read [AGENTS.md](AGENTS.md) first (it applies to people and AI agents alike).
2. Fork the repository and create a branch for your work.
3. For changes to a skill, test it before and after: run the scenario without your change, then with it, and record both in the fixture's `evaluations.md` (see *Testing expectations* in AGENTS.md).
4. Run the checks:

   ```sh
   sh scripts/validate-skills.sh
   python3 -I scripts/test_prepare_input.py
   ```

5. Open a pull request.

**Never include real personal data, conversation exports, or credentials.** Examples and tests use synthetic data only.

## Updating

**Claude Code:** `/plugin marketplace update craftapps`, then reinstall or restart if asked. **Other agents:** pull the latest version of this repository, or download it again.

## License

[MIT](LICENSE). Use, change, and share the skills freely.
