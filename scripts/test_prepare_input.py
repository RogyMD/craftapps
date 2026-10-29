"""Tests for skills/discover-app/scripts/prepare_input.py (standard library only).

Run from the repository root:  python3 -I scripts/test_prepare_input.py
"""

import contextlib
import importlib.util
import io
import json
import os
import pathlib
import random
import string
import sys
import tempfile
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills/discover-app/scripts/prepare_input.py"
FIXTURE = ROOT / "examples/discovery/synthetic-ios-developer/input"

sys.dont_write_bytecode = True  # keep skill folders free of __pycache__
spec = importlib.util.spec_from_file_location("prepare_input", SCRIPT)
prepare_input = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare_input)

PLANTED = ["KEYID-FAKE-7Q2X", "00000000-fake-issuer-0000", "FAKE-PRIVATE-KEY-DO-NOT-USE-9f8e7d",
           "dana.whitfield@example.com", "555 0142"]


def run(*args):
    """Run the script; return (stdout, cleaned file text)."""
    with tempfile.TemporaryDirectory() as tmp:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            prepare_input.main([*map(str, args), "--out", tmp])
        return out.getvalue(), (pathlib.Path(tmp) / "cleaned-input.md").read_text()


class RedactionTests(unittest.TestCase):
    def redact(self, text, terms=()):
        return prepare_input.Redactor(list(terms))(text)

    def test_secrets_are_redacted(self):
        samples = [
            "key sk-proj-AbCdEf0123456789XyZ0123",
            "token ghp_" + "a1B2" * 9,
            "aws AKIAABCDEFGHIJKLMNOP",
            "jwt eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N",
            "-----BEGIN PRIVATE KEY-----\nMIGTAgEAMBMG\n-----END PRIVATE KEY-----",
            "password: hunter22",
            "card 4111 1111 1111 1111",
            "hash 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
        ]
        for sample in samples:
            with self.subTest(sample=sample[:20]):
                self.assertIn("[REDACTED", self.redact(sample))
        self.assertNotIn("hunter22", self.redact("password: hunter22"))

    def test_contact_details_are_redacted(self):
        self.assertNotIn("a.b@example.org", self.redact("mail a.b@example.org"))
        self.assertNotIn("555-123-4567", self.redact("call 555-123-4567"))
        self.assertNotIn("+44 20 7946 0958", self.redact("call +44 20 7946 0958 today"))

    def test_url_query_is_redacted_but_host_kept(self):
        result = self.redact("see https://example.com/reset?token=abc123&user=7")
        self.assertIn("https://example.com/reset", result)
        self.assertNotIn("abc123", result)

    def test_listed_terms_are_redacted_case_insensitively(self):
        result = self.redact("Email DANA WHITFIELD today", terms=["Dana Whitfield"])
        self.assertNotIn("WHITFIELD", result)

    def test_everyday_text_is_untouched(self):
        for text in ["Released v2.3 on 2026-02-03", "takes ~20 minutes", "iOS 26 widget",
                     "Version 1.2.3.4", "under 500 characters", "Build 2026100401"]:
            with self.subTest(text=text):
                self.assertEqual(self.redact(text), text)

    def test_payment_sdk_keys_are_redacted(self):
        for key in ["appl_" + "Ab12Cd34Ef56Gh78Ij90", "goog_" + "Zy98Xw76Vu54Ts32Rq10",
                    "sk_live_" + "51Hfake" * 4, "rk_test_" + "a1b2c3d4" * 3]:
            with self.subTest(key=key[:8]):
                self.assertNotIn(key, self.redact("key " + key))

    def test_long_numbers_are_redacted_except_timestamps(self):
        for text, number in [("card 4111 1111 1111 1111", "4111 1111 1111 1111"),
                             ("order 4111111111111112", "4111111111111112"),
                             ("iban 9876543210987654321", "9876543210987654321"),
                             ("account 12345678901234", "12345678901234"),
                             ("iban MD24AG000225100013104168", "MD24AG000225100013104168"),
                             ("iban GB82 WEST 1234 5698 7654 32", "WEST 1234 5698 7654 32")]:
            with self.subTest(text=text):
                self.assertNotIn(number, self.redact(text))
        for text in ["ts 1729600000000", "id 20261022143055"]:
            with self.subTest(text=text):
                self.assertEqual(self.redact(text), text)

    def test_card_numbers_followed_by_more_digits_are_redacted(self):
        for text, card in [("card 4242 4242 4242 4242 12 27", "4242 4242 4242 4242"),
                           ("card 4532015112830366 123", "4532015112830366"),
                           ("5555 5555 5555 4444 123", "5555 5555 5555 4444")]:
            with self.subTest(text=text):
                self.assertNotIn(card, self.redact(text))

    def test_env_style_labels_are_redacted(self):
        for text, secret in [("AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                              "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"),
                             ("DB_PASSWORD=Tr0ub4dor-and-3-horses", "Tr0ub4dor-and-3-horses")]:
            with self.subTest(text=text[:12]):
                self.assertNotIn(secret, self.redact(text))

    def test_paths_branches_and_ids_are_kept(self):
        for text in ["/Users/sam/Projects/Plantly2026/Sources/WateringScheduleViewController2.swift",
                     "feature/plantly-2026-10-22-watering-widget-v2",
                     "sim 3F2504E0-4F89-11D3-9A0C-0305E82C3301",
                     "skills/discover-app/scripts/prepare_input.py"]:
            with self.subTest(text=text[:30]):
                self.assertEqual(self.redact(text), text)

    def test_random_tokens_are_still_redacted(self):
        for text in ["base64 aGVsbG8gd29ybGQgdGhpcyBpcyBhIGZha2Uga2V5MTIz",
                     "sha 3f2a9c4e1b7d8f6a5c3e2d1b0a9f8e7d6c5b4a39",
                     "blob abcDEF123+ghiJKL456/mnoPQR789+stuVWX012==",
                     "aws hT7kQ2xWm9Lp/R4vN8sJd3F/gB6yC1zXa5Ke0VuIo2",
                     "url-safe Qx3_vR9-kLm2Tz8_wNp4-Yh7Gd1_sKe5Uc6Bj0",
                     "url-safe2 k9_ZpQ-3vXr_8LmT-w2Yq_N5hJ-c7Ds4Xe"]:
            with self.subTest(text=text[:10]):
                self.assertIn("[REDACTED", self.redact(text))


    def test_single_case_random_tokens_are_redacted(self):
        rng = random.Random(7)
        for alphabet in (string.ascii_lowercase + string.digits,
                         string.ascii_uppercase + string.digits, string.ascii_uppercase + "234567"):
            tokens = ["".join(rng.choice(alphabet) for _ in range(40)) for _ in range(300)]
            leaked = [t for t in tokens if any(c.isdigit() for c in t) and t in self.redact("key " + t)]
            with self.subTest(alphabet=alphabet[:3]):
                self.assertLessEqual(len(leaked), 3, leaked[:3])


class FixtureTests(unittest.TestCase):
    def test_fixture_has_no_planted_secrets_and_no_assistant_text(self):
        stdout, cleaned = run(FIXTURE)
        for value in PLANTED:
            self.assertNotIn(value, cleaned)
            self.assertNotIn(value, stdout)
        self.assertNotIn("Translations follow", cleaned)  # assistant replies dropped
        self.assertIn("I do this every release", cleaned)  # user messages kept

    def test_stdout_never_contains_content(self):
        stdout, _ = run(FIXTURE)
        for phrase in ["release", "Pocket Plant", "Whitfield", "workout"]:
            self.assertNotIn(phrase, stdout)

    def test_redact_term_exclude_and_dates(self):
        _, cleaned = run(FIXTURE, "--redact-term", "Dana Whitfield", "--exclude", "workout",
                         "--since", "2026-03-01")
        self.assertNotIn("Whitfield", cleaned)
        self.assertNotIn("workout", cleaned.lower())
        self.assertNotIn("What's New text for 2.3", cleaned)  # 2026-02-03, before --since

    def test_reads_export_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = pathlib.Path(tmp) / "export.zip"
            with zipfile.ZipFile(archive, "w") as z:
                z.write(FIXTURE / "synthetic-claude-export.json", "conversations.json")
            stdout, cleaned = run(archive)
        self.assertIn("claude-export, 5 conversations kept", stdout)
        self.assertIn("Missing Japanese strings", cleaned)

    def test_unknown_json_reports_field_names_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            odd = pathlib.Path(tmp) / "odd.json"
            odd.write_text('[{"who": "me", "said": "my secret plan"}]')
            stdout, _ = run(odd)
        self.assertIn("unknown format", stdout)
        self.assertIn("said", stdout)
        self.assertNotIn("secret plan", stdout)


def write_jsonl(path, objects):
    """Write synthetic session-log lines (objects, or raw strings for broken lines)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(o if isinstance(o, str) else json.dumps(o) for o in objects) + "\n")
    return path


def cc(content, day="2026-10-01", **extra):
    """A synthetic Claude Code log line typed by the person (or shaped by extra fields)."""
    return {"type": "user", "sessionId": "s1", "timestamp": day + "T10:00:00Z", "entrypoint": "cli",
            "cwd": "/Users/sam/Projects/plantly", "message": {"role": "user", "content": content},
            **extra}


def cx_meta(originator="codex-tui", thread_source="user"):
    return {"timestamp": "2026-10-02T09:00:00Z", "type": "session_meta",
            "payload": {"id": "t1", "cwd": "/Users/sam/Projects/plantly", "originator": originator,
                        "thread_source": thread_source}}


def cx_item(kind, text):
    return {"timestamp": "2026-10-02T09:01:00Z", "type": "event_msg",
            "payload": {"type": "item_completed",
                        "item": {"type": kind, "content": [{"type": "text", "text": text}]}}}


CLAUDE_CODE_SESSION = [
    {"type": "summary", "summary": "x"},
    cc("Please rename the build scheme"),
    {"type": "assistant", "sessionId": "s1", "message": {"role": "assistant",
                                                         "content": [{"type": "text", "text": "Sure, renaming"}]}},
    cc([{"type": "tool_result", "content": "file listing"}]),
    cc("meta caveat", isMeta=True),
    cc("<command-name>/compact</command-name>\n<command-args>keep the release notes</command-args>"),
    cc("keep the release notes"),
    cc("<task-notification>task done</task-notification>"),
    cc("<bash-input>open -a Xcode</bash-input>"),
    cc("<bash-stdout>secret listing</bash-stdout>"),
    cc("Fix the widget<system-reminder>internal</system-reminder>"),
    cc("<pasted_content id=\"p1\">pasted log</pasted_content>\nwhy does this crash"),
    cc("subagent prompt", isSidechain=True),
    cc("[Request interrupted by user]"),
]

CODEX_SESSION = [
    cx_meta(),
    {"type": "response_item", "payload": {"type": "message", "role": "user", "content": [
        {"type": "input_text", "text": "<environment_context>sandbox</environment_context>"}]}},
    cx_item("UserMessage", "Add a watering reminder"),
    cx_item("AgentMessage", "Done too"),
    {"type": "response_item", "payload": {"type": "function_call_output", "output": "file listing"}},
]


class SessionLogTests(unittest.TestCase):
    def run_logs(self, *sessions, args=()):
        """Write each session as its own .jsonl in one folder; run the script on the folder."""
        with tempfile.TemporaryDirectory() as tmp:
            for i, lines in enumerate(sessions):
                write_jsonl(pathlib.Path(tmp) / "logs" / ("session-%d.jsonl" % i), lines)
            return run(pathlib.Path(tmp) / "logs", *args)

    def test_claude_code_keeps_only_typed_messages(self):
        _, cleaned = self.run_logs(CLAUDE_CODE_SESSION)
        for kept in ["Please rename the build scheme", "Fix the widget", "why does this crash",
                     "Claude Code · plantly"]:
            self.assertIn(kept, cleaned)
        self.assertEqual(cleaned.count("keep the release notes"), 1)
        for dropped in ["Sure, renaming", "file listing", "meta caveat", "task done", "open -a Xcode",
                        "secret listing", "internal", "pasted log", "subagent prompt",
                        "Request interrupted"]:
            self.assertNotIn(dropped, cleaned)

    def test_unclosed_pasted_content_is_removed(self):
        _, cleaned = self.run_logs([cc('see this <pasted_content id="p2">log line one\nlog line two')])
        self.assertIn("see this", cleaned)
        self.assertNotIn("log line", cleaned)
        self.assertNotIn("<pasted_content", cleaned)

    def test_claude_code_sdk_sessions_are_automated(self):
        stdout, cleaned = self.run_logs([cc("Run the nightly worker task", entrypoint="sdk-cli")])
        self.assertNotIn("nightly worker", cleaned)
        self.assertIn("1 automated", stdout)

    def test_other_claude_code_front_ends_are_kept(self):
        _, cleaned = self.run_logs([cc("Typed in the editor extension", entrypoint="claude-vscode")])
        self.assertIn("Typed in the editor extension", cleaned)

    def test_odd_shapes_and_unreadable_files_do_not_stop_the_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            logs = pathlib.Path(tmp) / "logs"
            write_jsonl(logs / "a-odd.jsonl", [
                {"type": "user", "sessionId": "s", "message": "just a string"},
                cc([{"type": "text", "text": None}, {"type": "text", "text": ["x"]}]),
                "[" * 100000 + "]" * 100000,
                cc("Kept after odd lines")])
            write_jsonl(logs / "b-codex.jsonl", [cx_meta(), {"type": "event_msg", "payload": {
                "type": "item_completed", "item": {"type": "UserMessage", "content": [
                    {"type": "text", "text": None}, {"type": "text", "text": "Codex kept"}]}}}])
            (logs / "c-dir.jsonl").mkdir()
            (logs / "d-broken.jsonl").symlink_to(logs / "missing-ProjectClientX.jsonl")
            write_jsonl(logs / "e-good.jsonl", [cc("Good session")])
            locked = write_jsonl(logs / "f-locked-ProjectClientX.jsonl", [cc("locked")])
            locked.chmod(0)
            err = io.StringIO()
            try:
                with contextlib.redirect_stderr(err):
                    stdout, cleaned = run(logs)
            finally:
                locked.chmod(0o600)
        for kept in ["Kept after odd lines", "Codex kept", "Good session"]:
            self.assertIn(kept, cleaned)
        self.assertNotIn("ProjectClientX", stdout + err.getvalue())
        self.assertIn("unreadable files", stdout)

    def test_codex_keeps_only_user_messages(self):
        _, cleaned = self.run_logs(CODEX_SESSION)
        self.assertIn("Add a watering reminder", cleaned)
        self.assertIn("Codex · plantly", cleaned)
        for dropped in ["sandbox", "Done too", "file listing"]:
            self.assertNotIn(dropped, cleaned)

    def test_codex_legacy_user_message_events(self):
        _, cleaned = self.run_logs([cx_meta(), {"type": "event_msg", "payload": {
            "type": "user_message", "message": "Sort my plant photos"}}])
        self.assertIn("Sort my plant photos", cleaned)

    def test_codex_exec_and_review_sessions_are_automated(self):
        stdout, cleaned = self.run_logs(
            [cx_meta(originator="codex_exec"), cx_item("UserMessage", "Batch job prompt")],
            [cx_meta(thread_source="guardian_review"), cx_item("UserMessage", "Review this diff")])
        self.assertNotIn("Batch job prompt", cleaned)
        self.assertNotIn("Review this diff", cleaned)
        self.assertIn("2 automated", stdout)

    def test_ide_context_does_not_hide_typed_words(self):
        _, cleaned = self.run_logs([cc([
            {"type": "text", "text": "<ide_opened_file>The user opened Login.swift</ide_opened_file>"},
            {"type": "text", "text": "Why does the login screen crash?"}]),
            cc("<ide_selection>let x = 1</ide_selection>\nWhat does this line do?")])
        self.assertIn("Why does the login screen crash?", cleaned)
        self.assertIn("What does this line do?", cleaned)
        self.assertNotIn("opened Login.swift", cleaned)
        self.assertNotIn("let x = 1", cleaned)

    def test_typed_html_and_caveats_are_kept(self):
        _, cleaned = self.run_logs([
            cc('<div class="row"> will not center, why?'),
            cc("Caveat: I'm on iOS 17, how do I add a widget?"),
            cc("Caveat: The messages below were generated by the user while running local commands. "
               "DO NOT respond to these messages")])
        self.assertIn("will not center", cleaned)
        self.assertIn("how do I add a widget", cleaned)
        self.assertNotIn("DO NOT respond", cleaned)

    def test_claude_code_log_with_a_long_preamble_is_read(self):
        preamble = [{"type": "summary", "summary": "s", "leafUuid": "u%d" % i} for i in range(25)]
        _, cleaned = self.run_logs(preamble + [cc("After the summaries")])
        self.assertIn("After the summaries", cleaned)

    def test_codex_interactive_sources_are_kept(self):
        _, cleaned = self.run_logs([cx_meta(thread_source="vscode"), cx_item("UserMessage", "From the editor")])
        self.assertIn("From the editor", cleaned)

    def test_title_redactions_are_counted_once(self):
        stdout, _ = self.run_logs([cc("Rename it", cwd="/Users/sam/acme-sam@example.com")])
        self.assertIn("email 1", stdout)

    def test_subagent_logs_are_not_counted_as_sessions(self):
        stdout, _ = self.run_logs([cc("Main session")], [cc("subagent prompt", isSidechain=True)])
        self.assertIn("sessions: 1 read, 1 kept", stdout)

    def test_session_log_text_is_redacted(self):
        _, cleaned = self.run_logs([cc("use key appl_Ab12Cd34Ef56Gh78Ij90")])
        self.assertNotIn("appl_Ab12Cd34Ef56Gh78Ij90", cleaned)

    def test_session_log_skips_broken_lines(self):
        stdout, cleaned = self.run_logs([cc("first message"), "{not json", cc("second message")])
        self.assertIn("second message", cleaned)
        self.assertIn("1 unreadable", stdout)

    def test_unknown_jsonl_reports_field_names_only(self):
        stdout, _ = self.run_logs([{"who": "me", "said": "my secret plan"}])
        self.assertIn("unknown format", stdout)
        self.assertIn("said", stdout)
        self.assertNotIn("secret plan", stdout)

    def test_session_filters_apply(self):
        old = [cc("Water the ferns", day="2026-09-01")]
        new = [cc("Plan my workout", day="2026-10-01")]
        _, cleaned = self.run_logs(old, new, args=("--since", "2026-09-15"))
        self.assertNotIn("ferns", cleaned)
        self.assertIn("workout", cleaned)
        stdout, cleaned = self.run_logs(old, new, args=("--exclude", "workout"))
        self.assertNotIn("workout", cleaned)
        self.assertIn("1 excluded", stdout)

    def test_index_lists_kept_sessions(self):
        _, cleaned = self.run_logs([cc("Rename the scheme"), cc("Bump the build number")])
        self.assertIn("## Index", cleaned)
        self.assertIn("· Claude Code · plantly · 2 messages", cleaned)
        _, cleaned = run(FIXTURE)
        index = cleaned.split("## Index", 1)[1].split("## Messages", 1)[0]
        self.assertRegex(index, r"- \d{4}-\d\d-\d\d · .+ · \d+ messages")

    def test_stdout_never_contains_session_content(self):
        stdout, _ = self.run_logs(CLAUDE_CODE_SESSION, CODEX_SESSION)
        for phrase in ["rename", "watering", "plantly", "Xcode"]:
            self.assertNotIn(phrase, stdout)


class FromHistoryTests(unittest.TestCase):
    """--from reads only the AI tool's own history folder (env overrides keep tests off ~)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        saved = {k: os.environ.get(k) for k in ("CLAUDE_CONFIG_DIR", "CODEX_HOME")}
        os.environ["CLAUDE_CONFIG_DIR"] = str(self.root / "claude")
        os.environ["CODEX_HOME"] = str(self.root / "codex")
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(lambda: [os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
                                 for k, v in saved.items()])

    def test_from_reads_default_folder(self):
        write_jsonl(self.root / "claude/projects/p/s.jsonl", [cc("Rename the scheme")])
        write_jsonl(self.root / "codex/sessions/2026/10/22/rollout-x.jsonl",
                    [cx_meta(), cx_item("UserMessage", "Add a watering reminder")])
        stdout, cleaned = run("--from", "claude-code", "--from", "codex")
        self.assertIn("Claude Code history: sessions: 1 read, 1 kept", stdout)
        self.assertIn("Codex history: sessions: 1 read, 1 kept", stdout)
        self.assertIn("Rename the scheme", cleaned)
        self.assertIn("Add a watering reminder", cleaned)

    def test_from_reads_only_session_logs(self):
        projects = self.root / "claude/projects/p"
        write_jsonl(projects / "s.jsonl", [cc("Rename the scheme")])
        (projects / "memory").mkdir()
        (projects / "memory/MEMORY.md").write_text("agent memory note")
        (projects / "s/tool-results").mkdir(parents=True)
        (projects / "s/tool-results/out.txt").write_text("saved tool output")
        (projects / "s/agent-x.meta.json").write_text('{"agentType": "Explore"}')
        stdout, cleaned = run("--from", "claude-code")
        self.assertIn("Rename the scheme", cleaned)
        self.assertNotIn("agent memory note", cleaned)
        self.assertNotIn("saved tool output", cleaned)
        self.assertNotIn("MEMORY.md", stdout)
        self.assertNotIn("agent-x", stdout)

    def test_from_missing_folder_reports_not_found(self):
        write_jsonl(self.root / "claude/projects/p/s.jsonl", [cc("Rename the scheme")])
        with tempfile.TemporaryDirectory() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = prepare_input.main(["--from", "codex", "--from", "claude-code", "--out", tmp])
            cleaned = (pathlib.Path(tmp) / "cleaned-input.md").read_text()
        self.assertEqual(code, 0)
        self.assertIn("Codex history: not found", out.getvalue())
        self.assertIn("Rename the scheme", cleaned)

    def test_paths_or_from_required(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            prepare_input.main([])


if __name__ == "__main__":
    unittest.main(verbosity=1)
