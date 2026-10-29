#!/usr/bin/env python3
"""Prepare private material for CraftApps Discovery, locally.

Runs entirely on your computer: no AI, no network, Python standard library only.

- Reads AI chat history exports (supported formats: ChatGPT and Claude
  conversations.json, or the export .zip), Markdown / plain-text files (which
  works for conversations copied from any other assistant), and the local
  history of AI coding tools: --from claude-code (~/.claude/projects) and
  --from codex (~/.codex/sessions). It reads only the folders you name.
- Keeps only YOUR messages: assistant replies, tool output, shell commands,
  notices, repeated messages, and sessions started by programs are dropped.
- Redacts secrets, emails, phone numbers, bank account, card and other long
  numbers, URL query strings, and any terms you list (for example people's names).
- Writes one Markdown file for you to review before any AI reads it.
- Prints only counts and file names, never content, so an AI agent can run it
  without seeing your conversations.

Usage:
  python3 -I prepare_input.py [PATH ...] [--from claude-code|codex] [--out DIR]
      [--redact-term TERM ...] [--exclude KEYWORD ...]
      [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--max-chars N]

Automatic redaction is not perfect. Names of people are only removed when
passed with --redact-term. Always review the output.
"""

import argparse
import collections
import datetime
import itertools
import json
import os
import pathlib
import re
import sys
import zipfile

TEXT_SUFFIXES = {".md", ".markdown", ".txt"}

# Order matters: multi-line and specific patterns run before generic ones.
PATTERNS = [
    ("private key block", re.compile(
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S)),
    ("known token", re.compile(
        r"\b(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"
        r"|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|xox[abprs]-[A-Za-z0-9-]{10,}"
        r"|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
        r"|(?:sk|rk|pk)_(?:live|test)_[A-Za-z0-9]{16,}|(?:appl|goog|amzn|strp|rcb)_[A-Za-z0-9]{16,})")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("url query", re.compile(r"(?<=[^\s?#])\?[^\s)\]>\"']+")),
    ("bank account", re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,4})?\b")),
    ("card or account number", re.compile(r"(?<!\d)\d(?:[ -]?\d){12,}(?!\d)")),
    ("phone", re.compile(
        r"(?<![\w.])(?:\+\d[\d ().-]{6,}\d|\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4})(?![\w.])")),
    ("long secret-like string", re.compile(
        r"\b(?=[A-Za-z0-9+/_-]*\d)(?=[A-Za-z0-9+/_-]*[A-Za-z])[A-Za-z0-9+/_-]{32,}={0,2}")),
]

# Some matches are kept: a long number that is a timestamp, and a "long
# secret-like string" that reads like words (see looks_random).
CHECKS = {
    "card or account number": lambda m: not timestamp_like(m.group()),
    "long secret-like string": lambda m: looks_random(m.group()),
}
UUID = re.compile(r"[0-9A-Fa-f]{8}(?:-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12}")
HEX_RUN = re.compile(r"[0-9A-Fa-f]{32,}")


def timestamp_like(text):
    """True for a time written as one run of digits: milliseconds since 1970
    (13 digits, 2001-2036) or YYYYMMDDhhmmss. Every other long number may be a
    card, bank account, or ID number, so it is redacted."""
    if not text.isdigit():
        return False
    if len(text) == 13:
        return 10 ** 12 <= int(text) < 21 * 10 ** 11
    if len(text) == 14:
        try:
            return 1970 <= datetime.datetime.strptime(text, "%Y%m%d%H%M%S").year < 2100
        except ValueError:
            return False
    return False


def char_kind(ch):
    return "upper" if ch.isupper() else "lower" if ch.islower() else "digit"


CONSONANT_RUN = re.compile(r"[b-df-hj-np-tv-xz]{6,}", re.I)  # words rarely stack six consonants


def letter_digit_switches(token):
    """How often letters and digits alternate inside one part of a path or name.
    Names put digits at the edges (Plantly2026, v2); random keys scatter them."""
    return sum(a.isdigit() != b.isdigit() for part in re.split(r"[/_-]", token)
               for a, b in zip(part, part[1:]))


def looks_random(token):
    """Keep paths, branch names, file names, and UUIDs; redact random-looking tokens.
    Random keys switch between upper case, lower case, and digits at almost every
    character (measured: 99% of random keys switch at 40% or more of characters;
    paths and CamelCase names at most about 34%). Keys in one letter case switch
    less, but still mix letters and digits throughout, or stack consonants no
    word has. Hex keys are redacted on their own."""
    if UUID.fullmatch(token):
        return False
    if "+" in token or token.endswith("=") or HEX_RUN.search(token):
        return True
    chars = re.sub(r"[/_-]", "", token)
    switches = sum(char_kind(a) != char_kind(b) for a, b in zip(chars, chars[1:]))
    return (switches >= 0.38 * max(1, len(chars) - 1) or letter_digit_switches(token) >= 6
            or bool(CONSONANT_RUN.search(chars)))


# A value that follows a secret-sounding word: "API key: abc123", "password is hunter22".
# Labels may sit inside environment-variable names: AWS_SECRET_ACCESS_KEY=..., DB_PASSWORD=...
# Deliberately aggressive: over-redacting a harmless word is better than leaking a secret.
CONTEXT_SECRET = re.compile(
    r"(?i)(?<![A-Za-z])(api[ _-]?key|access[ _-]?key|secret[ _-]?key|key[ _-]?id|private[ _-]?key"
    r"|secret|token|password|passcode|passwd|pwd|issuer(?:[ _-]?id)?|client[ _-]?secret)(?![A-Za-z])"
    r"([A-Za-z0-9_]*\s*(?:is|[:=])?\s*)([^\s,;]{6,})")


class Redactor:
    def __init__(self, terms):
        self.counts = {}
        self.terms = [re.compile(re.escape(t), re.I) for t in terms if t.strip()]

    def _sub(self, label, pattern, text, repl):
        check = CHECKS.get(label)

        def replace(match):
            if check and not check(match):
                return match.group()
            self.counts[label] = self.counts.get(label, 0) + 1
            return repl(match) if callable(repl) else match.expand(repl)

        return pattern.sub(replace, text)

    def __call__(self, text):
        for pattern in self.terms:
            text = self._sub("listed term", pattern, text, "[REDACTED: term]")
        text = self._sub("secret after keyword", CONTEXT_SECRET, text,
                         lambda m: m.group(1) + m.group(2) + "[REDACTED: secret]")
        for label, pattern in PATTERNS:
            if label == "url query":
                text = self._sub(label, pattern, text, "?[REDACTED: query]")
            else:
                text = self._sub(label, pattern, text, "[REDACTED: %s]" % label)
        return text


def parse_day(value):
    return datetime.date.fromisoformat(value) if value else None


def epoch_to_day(value):
    try:
        return datetime.datetime.fromtimestamp(float(value), datetime.timezone.utc).date()
    except (TypeError, ValueError, OverflowError, OSError):
        return None


def iso_to_day(value):
    try:
        return datetime.date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def chatgpt_conversations(data):
    """Yield (day, title, [user messages]) from a ChatGPT conversations.json."""
    for conv in data:
        nodes = [n.get("message") for n in (conv.get("mapping") or {}).values()]
        msgs = [m for m in nodes if m and (m.get("author") or {}).get("role") == "user"]
        msgs.sort(key=lambda m: m.get("create_time") or 0)
        texts = []
        for m in msgs:
            parts = (m.get("content") or {}).get("parts") or []
            text = "\n".join(p for p in parts if isinstance(p, str)).strip()
            if text:
                texts.append(text)
        yield epoch_to_day(conv.get("create_time")), conv.get("title") or "Untitled", texts


def claude_conversations(data):
    """Yield (day, title, [user messages]) from a Claude conversations.json."""
    for conv in data:
        texts = []
        for m in conv.get("chat_messages") or []:
            if m.get("sender") != "human":
                continue
            text = (m.get("text") or "").strip()
            if not text:
                text = "\n".join(c.get("text", "") for c in m.get("content") or []
                                 if isinstance(c, dict) and c.get("type") == "text").strip()
            if text:
                texts.append(text)
        yield iso_to_day(conv.get("created_at")), conv.get("name") or "Untitled", texts


# --- AI tool session logs (.jsonl, one session per file) ---
# Only what the person typed is kept. Tool output, file contents, shell commands,
# notices, and the agent's own text are dropped, and so are sessions a program
# started (they are not the person's words).

Session = collections.namedtuple("Session", "day title texts dropped automated subagent")
REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
IDE_CONTEXT = re.compile(r"<(ide_[a-z_]+)\b[^>]*>.*?</\1>", re.S)  # what the editor attaches
PASTED = re.compile(r"<pasted_content\b.*?(?:</pasted_content>|\Z)", re.S)  # may be cut off
COMMAND_ARGS = re.compile(r"<command-args>(.*?)</command-args>", re.S)
# Tools wrap their output in tags with - or _ in the name (<bash-stdout>, <command-name>);
# HTML a person types (<div>) has neither, so it is kept.
LEADING_TAG = re.compile(r"<[a-z][a-z0-9]*[-_][a-z0-9_-]*[\s>/]")
NOT_TYPED = ("[Request interrupted", "Caveat: The messages below were generated",
             "This session is being continued from a previous conversation")


def block_text(blocks, block_type):
    """Join the text of blocks of one type; ignores anything that is not text."""
    if not isinstance(blocks, list):
        return ""
    return "\n".join(b["text"] for b in blocks if isinstance(b, dict)
                     and b.get("type") == block_type and isinstance(b.get("text"), str))


def clean_typed(text, seen, dropped):
    """Return the person's own words from one message, or None (counted in dropped)."""
    text = PASTED.sub("[pasted text removed]", IDE_CONTEXT.sub("", REMINDER.sub("", text))).strip()
    if not text:
        return None
    if LEADING_TAG.match(text) or text.startswith(NOT_TYPED):
        dropped["tool or command output"] += 1
        return None
    key = " ".join(text.split())
    if key in seen:
        dropped["repeat"] += 1
        return None
    seen.add(key)
    return text


def session_title(tool, cwd, fallback_name):
    name = pathlib.PurePath(cwd).name if isinstance(cwd, str) and cwd else ""
    return "%s · %s" % (tool, name) if name else fallback_name


def claude_code_session(objects, fallback_name):
    texts, seen, dropped = [], set(), collections.Counter()
    day = cwd = entrypoint = None
    main_thread = False
    for obj in objects:
        cwd = cwd or obj.get("cwd")
        entrypoint = entrypoint or obj.get("entrypoint")
        if obj.get("type") in ("user", "assistant") and not obj.get("isSidechain"):
            main_thread = True
        if obj.get("type") != "user" or obj.get("isMeta") or obj.get("isSidechain") \
                or obj.get("isCompactSummary") or obj.get("toolUseResult") is not None:
            continue
        message = obj.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if isinstance(content, list):
            if any(isinstance(c, dict) and c.get("type") == "tool_result" for c in content):
                dropped["tool or command output"] += 1
                continue
            content = block_text(content, "text")
        if not isinstance(content, str):
            continue
        args = COMMAND_ARGS.search(content)
        if args:  # a slash command: keep only what the person wrote after it
            content = args.group(1)
            if not content.strip():
                dropped["tool or command output"] += 1
                continue
        text = clean_typed(content, seen, dropped)
        if text:
            day = day or iso_to_day(obj.get("timestamp"))
            texts.append(text)
    # Non-interactive runs (claude -p, the Agent SDK) report "sdk-…"; editors and apps keep theirs.
    automated = isinstance(entrypoint, str) and entrypoint.startswith("sdk")
    # A log with only side-chain lines is a subagent's transcript, not a session the person had.
    return Session(day, session_title("Claude Code", cwd, fallback_name), texts, dropped, automated,
                   not main_thread)


# Codex sessions a program started; anything else (user, cli, vscode, …) is the person's.
AUTOMATED_SOURCES = ("exec", "review", "guardian", "subagent", "automation", "sdk", "mcp")


def codex_session(objects, fallback_name):
    texts, seen, dropped = [], set(), collections.Counter()
    day = cwd = None
    automated = False
    for obj in objects:
        payload = obj.get("payload")
        if not isinstance(payload, dict):
            continue
        if obj.get("type") == "session_meta":
            cwd = payload.get("cwd")
            sources = "%s %s" % (payload.get("thread_source") or "", payload.get("source") or "")
            automated = (payload.get("originator") == "codex_exec"
                         or any(hint in sources.lower() for hint in AUTOMATED_SOURCES))
            continue
        if obj.get("type") != "event_msg":
            continue
        item = payload.get("item") if payload.get("type") == "item_completed" else None
        if isinstance(item, dict) and item.get("type") == "UserMessage":
            content = block_text(item.get("content"), "text")
        elif payload.get("type") == "user_message":  # older Codex versions
            content = payload.get("message")
        else:
            continue
        text = clean_typed(content, seen, dropped) if isinstance(content, str) else None
        if text:
            day = day or iso_to_day(obj.get("timestamp"))
            texts.append(text)
    return Session(day, session_title("Codex", cwd, fallback_name), texts, dropped, automated, False)


def json_lines(handle, bad):
    """Yield each JSON object line; count broken lines in bad["unreadable"]."""
    for line in handle:
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            obj = None
        if isinstance(obj, dict):
            yield obj
        else:
            bad["unreadable"] += 1


CODEX_TYPES = {"session_meta", "event_msg", "response_item", "turn_context"}


def detect_jsonl(objects):
    for obj in objects:
        if "sessionId" in obj:
            return "claude-code"
        if "payload" in obj and obj.get("type") in CODEX_TYPES:
            return "codex"
    return None


HISTORY = {  # --from source: (label, config folder variable, default config folder, logs subfolder)
    "claude-code": ("Claude Code history", "CLAUDE_CONFIG_DIR", "~/.claude", "projects"),
    "codex": ("Codex history", "CODEX_HOME", "~/.codex", "sessions"),
}


def history_folder(source):
    """The one folder --from SOURCE reads. Nothing else on the computer is searched."""
    _, variable, default, logs = HISTORY[source]
    return pathlib.Path(os.environ.get(variable) or default).expanduser() / logs


def detect(data):
    if isinstance(data, list) and data and isinstance(data[0], dict):
        if "mapping" in data[0]:
            return "chatgpt-export", chatgpt_conversations
        if "chat_messages" in data[0]:
            return "claude-export", claude_conversations
    return None, None


def describe_shape(data):
    """Field names only, never values, to help adapt to an unknown format."""
    if isinstance(data, list):
        first = data[0] if data else None
        keys = sorted(first.keys()) if isinstance(first, dict) else type(first).__name__
        return "list of %d; first item fields: %s" % (len(data), keys)
    if isinstance(data, dict):
        return "object; fields: %s" % sorted(data.keys())
    return type(data).__name__


class Preparer:
    def __init__(self, args):
        self.args = args
        self.redact = Redactor(args.redact_term)
        self.excludes = [k.lower() for k in args.exclude]
        self.since, self.until = parse_day(args.since), parse_day(args.until)
        self.sections = []
        self.index = []
        self.summary = []
        self.log_stats = collections.defaultdict(collections.Counter)
        self.bad_files = 0

    def clip(self, text):
        limit = self.args.max_chars
        if limit and len(text) > limit:
            return text[:limit] + "\n[… %d characters removed]" % (len(text) - limit)
        return text

    def add_json(self, name, raw):
        try:
            data = json.loads(raw)
        except ValueError:
            self.summary.append("%s: skipped (not valid JSON)" % name)
            return
        kind, reader = detect(data)
        if not reader:
            self.summary.append("%s: skipped (unknown format: %s)" % (name, describe_shape(data)))
            return
        kept, excluded, messages = self.add_conversations(name, kind, reader(data))
        self.summary.append("%s: %s, %d conversations kept, %d excluded, %d of your messages"
                            % (name, kind, kept, excluded, messages))

    def add_conversations(self, name, kind, conversations):
        """Filter, redact, and add (day, title, texts) items. Returns (kept, excluded, messages)."""
        kept = excluded = messages = 0
        for day, title, texts in conversations:
            if not texts:
                continue
            if (self.since and day and day < self.since) or (self.until and day and day > self.until):
                excluded += 1
                continue
            haystack = (title + "\n" + "\n".join(texts)).lower()
            if any(k in haystack for k in self.excludes):
                excluded += 1
                continue
            kept += 1
            messages += len(texts)
            title = self.redact(title)
            self.index.append("- %s · %s · %d messages" % (day or "undated", title, len(texts)))
            body = "\n\n".join("> " + self.clip(self.redact(t)).replace("\n", "\n> ") for t in texts)
            self.sections.append("### %s · %s\n\nSource: %s (%s)\n\n%s" % (
                day or "undated", title, name, kind, body))
        return kept, excluded, messages

    def add_session_log(self, path):
        """One .jsonl session log. A file that cannot be read is counted, never shown:
        error messages would name the file, and the name can be private."""
        try:
            self._add_session_log(path)
        except (OSError, RecursionError, ValueError, TypeError, AttributeError):
            self.bad_files += 1

    def _add_session_log(self, path):
        """Stream one .jsonl session log line by line (logs can be very large)."""
        bad = collections.Counter()
        with open(path, encoding="utf-8", errors="replace") as handle:
            lines = json_lines(handle, bad)
            head = []                 # summary lines can come first, many of them
            for obj in itertools.islice(lines, 5000):
                head.append(obj)
                kind = detect_jsonl([obj])
                if kind:
                    break
            else:
                kind = None
            if not kind:
                self.summary.append("%s: skipped (unknown format: %s)"
                                    % (path.name, describe_shape(head[0] if head else None)))
                return
            reader = claude_code_session if kind == "claude-code" else codex_session
            session = reader(itertools.chain(head, lines), path.stem)
        if session.subagent:
            return
        stats = self.log_stats[kind]
        stats["unreadable"] += bad["unreadable"]
        stats["read"] += 1
        stats.update(session.dropped)
        if session.automated:
            stats["automated"] += 1
            return
        kept, excluded, messages = self.add_conversations(
            path.name, kind, [(session.day, session.title, session.texts)])
        stats["kept"] += kept
        stats["excluded"] += excluded
        stats["messages"] += messages

    def add_text(self, name, raw):
        lowered = raw.lower()
        if any(k in lowered for k in self.excludes):
            self.summary.append("%s: excluded (matched an --exclude keyword)" % name)
            return
        self.sections.append("### File: %s\n\n%s" % (name, self.clip(self.redact(raw.strip()))))
        self.summary.append("%s: text file, included" % name)

    def add_zip(self, path):
        with zipfile.ZipFile(path) as archive:
            members = [m for m in archive.namelist() if m.endswith("conversations.json")]
            if not members:
                self.summary.append("%s: skipped (no conversations.json inside)" % path.name)
            for member in members:
                self.add_json("%s/%s" % (path.name, member), archive.read(member).decode("utf-8"))

    def add_path(self, path, label=None, logs_only=False):
        """Add a file or folder. logs_only (for --from): read session logs (*.jsonl) and
        nothing else - those folders also hold tool output and agent notes."""
        self.log_stats.clear()
        self.bad_files = 0
        if logs_only:
            for log in sorted(path.rglob("*.jsonl")):
                if log.is_file():
                    self.add_session_log(log)
        else:
            self._add_path(path)
        if self.bad_files:
            self.summary.append("%s: %d unreadable files skipped" % (label or path.name, self.bad_files))
        for kind, stats in sorted(self.log_stats.items()):
            self.summary.append(
                "%s: sessions: %d read, %d kept, %d automated, %d excluded; your messages: %d; "
                "left out: %d tool or command outputs, %d repeats, %d unreadable lines" % (
                    label or path.name, stats["read"], stats["kept"], stats["automated"],
                    stats["excluded"], stats["messages"], stats["tool or command output"],
                    stats["repeat"], stats["unreadable"]))

    def _add_path(self, path):
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and not any(p.startswith(".") for p in child.relative_to(path).parts):
                    self.add_file(child)
        elif path.is_file():
            self.add_file(path)
        else:
            self.summary.append("%s: not found" % path)

    def add_file(self, path):
        suffix = path.suffix.lower()
        if suffix == ".zip":
            self.add_zip(path)
        elif suffix == ".json":
            self.add_json(path.name, path.read_text(encoding="utf-8"))
        elif suffix == ".jsonl":
            self.add_session_log(path)
        elif suffix in TEXT_SUFFIXES:
            self.add_text(path.name, path.read_text(encoding="utf-8", errors="replace"))
        else:
            self.summary.append("%s: skipped (unsupported type)" % path.name)

    def write(self, out_dir):
        out_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(out_dir, 0o700)
        out_file = out_dir / "cleaned-input.md"
        header = (
            "<!-- Prepared locally by discover-app/scripts/prepare_input.py on %s. -->\n\n"
            "# Cleaned input — review before sharing\n\n"
            "Only your own messages are included. Secrets, emails, phone numbers, account and card numbers, "
            "and listed terms were redacted automatically. **Automatic redaction is not perfect:** "
            "people's names and other private details may remain. Read this file, delete or edit "
            "anything you don't want an AI model to see, then tell your agent to go ahead.\n\n"
            % datetime.date.today().isoformat())
        fd = os.open(out_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(header + "## Index\n\n" + ("\n".join(self.index) or "(nothing kept)")
                         + "\n\n## Messages\n\n" + "\n\n".join(self.sections) + "\n")
        return out_file


def main(argv=None):
    parser = argparse.ArgumentParser(description="Prepare private material locally for Discovery.")
    parser.add_argument("paths", nargs="*", type=pathlib.Path, help="files or folders to prepare")
    parser.add_argument("--from", dest="sources", action="append", default=[], choices=sorted(HISTORY),
                        help="also read this AI tool's local history folder (repeatable)")
    parser.add_argument("--out", type=pathlib.Path, default=pathlib.Path("craftapps/cleaned"),
                        help="output folder (default: craftapps/cleaned)")
    parser.add_argument("--redact-term", action="append", default=[],
                        help="text to redact everywhere, e.g. a person's name (repeatable)")
    parser.add_argument("--exclude", action="append", default=[],
                        help="drop conversations or files containing this keyword (repeatable)")
    parser.add_argument("--since", help="keep conversations on or after YYYY-MM-DD")
    parser.add_argument("--until", help="keep conversations on or before YYYY-MM-DD")
    parser.add_argument("--max-chars", type=int, default=2000,
                        help="truncate each message to N characters; 0 = no limit (default 2000)")
    args = parser.parse_args(argv)
    if not args.paths and not args.sources:
        parser.error("give at least one PATH or --from")

    prep = Preparer(args)
    for path in args.paths:
        prep.add_path(path)
    for source in args.sources:
        label, folder = HISTORY[source][0], history_folder(source)
        if folder.is_dir():
            prep.add_path(folder, label, logs_only=True)
        else:
            prep.summary.append("%s: not found at %s" % (label, folder))
    out_file = prep.write(args.out)

    # Counts and names only. Never print content.
    print("Prepared locally (no network, no AI).")
    for line in prep.summary:
        print("  " + line)
    print("Redactions: " + (", ".join("%s %d" % kv for kv in sorted(prep.redact.counts.items()))
                            or "none"))
    print("Output: %s" % out_file)
    print("Next: open the output, remove anything you don't want shared, then tell your agent to go ahead.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
