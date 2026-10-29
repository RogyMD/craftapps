# Input formats

How each kind of input is handled. **Security rule:** the agent never opens raw conversation exports or AI tool session logs — not with a file reader, `cat`, `head`, `jq`, or any other command that would show their content. Only the local cleanup script touches them.

## Conversation exports → local cleanup

Supported by `scripts/prepare_input.py` (Python 3 standard library; no network, no AI). Formats supported today:

| Source | How the user gets it | What to pass |
|---|---|---|
| ChatGPT | Settings → Data controls → Export data (emailed ZIP) | The ZIP, or the unzipped folder |
| Claude | Settings → Privacy → Export data (emailed ZIP) | The ZIP, or the unzipped folder |

Run from the user's chosen working folder:

```sh
python3 -I <skill-dir>/scripts/prepare_input.py ~/Downloads/chatgpt-export.zip \
  --out craftapps/cleaned \
  --redact-term "Person Name" --exclude "health" --since 2026-01-01
```

Options: `--redact-term` (repeatable; names, companies, places), `--exclude` (repeatable; drops whole conversations containing the keyword), `--since` / `--until` (dates), `--max-chars` (truncates long pasted messages; default 2000).

**Any other AI assistant:** ask the user to copy the conversations they want analyzed into a `.txt` or `.md` file and pass that file through the script. It is redacted the same way.

What the script does:

- Keeps only the user's own messages; drops assistant replies, system and tool messages.
- Redacts private key blocks, common API token formats, values after words like "key", "token", "password", "secret", emails, phone numbers, bank account numbers (IBAN), card numbers and any other number of 13 or more digits (except timestamps), URL query strings, long random-looking strings, and listed terms.
- Writes `craftapps/cleaned/cleaned-input.md` readable only by the user (file mode 600).
- Prints only file names, counts, and redaction totals — never content.

What it does **not** do: detect people's names, health or financial details, or other context-dependent private information. That is why the user reviews the file.

After running:

1. Tell the user where the file is and what was redacted (from the printed counts).
2. Ask them to read it, delete or edit anything they don't want shared, and tell you to go ahead. Any clear yes counts; if the reply is unclear, ask once.
3. Only then read the cleaned file.

If `python3` is missing, tell the user how to install Python 3 for their operating system, or fall back to the interview mode. Do not read the raw export as a workaround.

### Unknown formats

If the script reports `unknown format`, it prints only the field names it found. Tell the user the format isn't supported yet. Options: interview mode, or the user copies the relevant messages into a text file themselves and passes it through the script. Do not open the raw file.

## AI tool history on this computer → local cleanup

Some AI coding tools keep every session on the computer as session logs (JSONL files). These logs mix the person's messages with tool output, file contents, shell commands, and sometimes secrets, so the agent never opens them. The script reads only the folder of the tool the person chose:

| Tool | Option | Folder it reads |
|---|---|---|
| Claude Code | `--from claude-code` | `~/.claude/projects` (or `$CLAUDE_CONFIG_DIR/projects`) |
| Codex | `--from codex` | `~/.codex/sessions` (or `$CODEX_HOME/sessions`) |

```sh
python3 -I <skill-dir>/scripts/prepare_input.py --from claude-code --out craftapps/cleaned \
    --redact-term "<name>" --exclude "<topic>"
```

Both options can be given at once, together with exports and the other options above. The script keeps only what the person typed. It drops the agent's replies, tool output, shell commands and their output, task notices, pasted blocks, repeated messages within a session, and sessions started by programs (non-interactive runs, automated reviewers). The cleaned file starts with an index of sessions (date, project folder name, number of messages), so the person can find and delete whole sessions.

If the agent's own permissions or sandbox refuse the command, give the person the exact line to run themselves. Never work around the refusal.

Sessions started by another tool typing into an interactive session cannot be told apart from the person's own. If the person spots them in the index, they can delete them or rerun with `--exclude "<a phrase those sessions start with>"`.

## Notes, journals, plain text, Markdown

Pass them through the script too (it redacts and wraps them into the same cleaned file), unless the user confirms they contain nothing sensitive. Treat headings, dates, and checklists as structure. Recurring entries ("every Monday…", "again had to…") and unchecked tasks that reappear are strong signals.

## App lists and workflow descriptions

Usually written for this purpose by the user; read directly. These are the main source for rung 0 (an existing tool already solves it) and for friction ("I use X but…").

## Projects and existing apps

Use only for folders the user points to. Read; never run, build, or modify anything.

Good signals:

| Look at | Signal |
|---|---|
| `README`, docs, notes | What the project is for; stated pain points and wishes |
| `TODO`, `FIXME`, `HACK` comments | Unfinished needs (`grep -rn "TODO\|FIXME" <folder>`) |
| Scripts folders, Makefiles, Shortcuts exports | Tasks already partly automated — often a sign of more to automate |
| `git log --oneline` | Repeated chores ("bump version", "update translations", "fix release notes") and their dates |
| Existing apps the user built | Improvements to them, or small complementary tools around them |
| Issue lists, changelogs | Recurring bug types or requests |

Never open: `.env` files, keychains, certificates, private keys (`*.p8`, `*.p12`, `*.pem`), provisioning profiles, credential or config files with secrets, build output, dependency folders (`node_modules`, `Pods`, `.build`), or large binary files. If a file name suggests secrets, skip it and mention it in the privacy notes.

## Large inputs

The cleaned file is much smaller than the raw export. Read it in parts of about 1,000 lines and send the person one progress line after each part ("Read 3 of 8 parts — 2 patterns so far"). If it is still too large to read fully:

1. Read the list of conversation headings (dates and titles) first.
2. Then read conversations whose titles match emerging patterns, plus an evenly spaced sample.
3. Record coverage in the report (for example "read 412 of 1,380 cleaned conversations; headings of all").
4. Counts from a sample are lower bounds. Say so.

The user can also narrow the input with `--since`, `--until`, and `--exclude`.
