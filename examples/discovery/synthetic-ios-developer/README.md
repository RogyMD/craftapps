# Fixture: synthetic iOS developer

**All data in this folder is synthetic.** The person, apps ("Pocket Plant Log", "Tide Timer", "Focus Jar"), client, keys, and contact details are invented for testing.

## Persona

An independent iOS developer with three small apps. Uses iPhone, iPad, and a Mac. Uses ChatGPT and Claude for release chores, writes notes in Markdown, tracks crashes in Numbers.

## Input

| File | Format | Contents |
|---|---|---|
| `input/synthetic-chatgpt-export.json` | ChatGPT export (`conversations.json` shape) | 5 conversations, Feb–Jun 2026 |
| `input/synthetic-claude-export.json` | Claude export (`conversations.json` shape) | 5 conversations, Jul–Sep 2026 |
| `input/notes.md` | Markdown notes | Release checklist, Monday routine, ideas |
| `input/apps-i-use.md` | App list | Devices, tools, friction |

## How to run

In a fresh agent session with the `discover-app` skill available, from the repository root:

> Use discover-app on `examples/discovery/synthetic-ios-developer/input/`. No exclusions, no names to redact. My devices: iPhone, iPad, Mac. Write output to `craftapps/` (it is git-ignored).

When the agent asks you to review `craftapps/cleaned/cleaned-input.md`, approve it unchanged; the test checks that the agent waits for approval and that the report still hides the client's name.

Then score the output against [`expected-findings.md`](expected-findings.md).

[`../../../skills/discover-app/examples/sample-report.md`](../../../skills/discover-app/examples/sample-report.md) is a reference report for this fixture. Your run does not need to match it word for word; it must satisfy the rubric.
