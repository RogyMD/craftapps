# Evaluations — local AI history scenarios

Results of running `discover-app` on the scenarios in [`expected-findings.md`](expected-findings.md).

## 2026-10-23 — baseline (skill before the change)

**Setup:** one fresh Claude Code subagent (Claude Opus 5.5) per scenario, given a copy of the skill as it was before this change (`SKILL.md` and `references/`) and the scenario text, told to run no commands and read nothing outside the skill folder. Scored by the maintainer's session.

| Scenario | Result | What the agent did |
|---|---|---|
| S1 first message | ❌ S1a, S1d, S1e · ✅ S1b (partly), S1c, S1f | Offered "AI chat history exports" as an optional add-on, never the person's local AI tool history. Asked about devices first. |
| S2 approval | ✅ S2a, S2b | Read on "looks good, go ahead" and held on "hmm, there's a lot in there". But the reply to the unclear case ended with *reply "approved" and I'll read it*: the skill only ever names the word "approved". |
| S3 progress | ❌ S3a · ✅ S3b | One message, then eight silent reads ("The person gets one message before many minutes of silence"). The skill's "choose a sampling plan" and the reference's "too large to read fully" were read differently. |
| S4 blocked command | ❌ S4a, S4b · ✅ S4c | Refused to use the history at all, quoting "Agent session logs (JSONL): Not supported yet", and asked the person to copy their typed requests into a text file by hand. |
| S5 devices | ✅ S5a · ⚠️ S5b · ❌ S5c | Left `user_devices` empty ("as stated by the user") and spread devices across Observed/Inferred/Assumed labels; never asked the person to confirm them. |

**Rationalizations quoted:** "I didn't ask which mode to use because the person already asked for an interview" (S1); "Running it on ~/.claude would have no supported purpose" (S4); "eight reads cover all of it, so it is not 'too large to read fully'" (S3).

## 2026-10-23 — with the change

**Setup:** same as the baseline, with the edited skill.

**Result: all rubric items pass (S1a–f, S2a–b, S3a–b, S4a–c, S5a–c).**

| Scenario | What the agent did |
|---|---|
| S1 first message | Listed the four sources in order, starting with "The history your AI tools keep on this computer: Claude Code (`~/.claude/projects`) and Codex (`~/.codex/sessions`). You don't need to export anything." No command run, no devices question, privacy statement included. |
| S2 approval | Read on "looks good, go ahead" ("looks good" and "go ahead" are both in its list). On "hmm, there's a lot in there" it did not read, asked once, offered `--since`/`--exclude`, and ended with *Just tell me "go ahead," or what you'd like removed.* |
| S3 progress | Said up front "8 parts … I'll send you one line after each part", then sent "Read N of 8 parts. K patterns so far." after every read; stated full coverage. |
| S4 blocked command | Ran `--from claude-code`; on refusal gave the exact one-line command, said it would not get around the block, and asked for the counts and a "go ahead". |
| S5 devices | Asked nothing before the report; wrote `user_devices: [iPhone (inferred), Mac (inferred), Apple Watch (inferred)]` with evidence; asked to confirm the list in the checkpoint message. |

**Gaps the agents noticed (not fixed; minor):** how to treat a device seen only once (the agent kept it, marked it weaker, and asked about it by name); what to do if the second reply after an unclear one is still unclear (the agent kept not reading). Three of the ten agents ran an `ls` on the skill folder despite being told to run no commands; none touched anything outside it.

**Limitations:** simulated conversations with pre-written replies, one run per scenario, one model. A real Claude Code permission refusal was seen in the 2026-10-22 maintainer test, not in these runs.
