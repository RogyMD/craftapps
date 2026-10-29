# Assessment rules

Use these definitions so reports are consistent and comparable.

## Claim labels

| Label | Meaning | Example |
|---|---|---|
| **Observed** | Directly present in the input, including the user's own interview answers | "Asked to translate release notes into 5 languages (O3, O7, O12)." |
| **Inferred** | Reasoned from observations; state the reasoning | "Likely happens every release, since requests align with version numbers." |
| **Assumed** | Not supported by the input; must be confirmed by the user | "Assumes release notes are written on a Mac." |

Never upgrade a label. When unsure, use the weaker one.

## Evidence strength

| Rating | Criteria |
|---|---|
| **Strong** | 3+ observations from distinct conversations or entries, or an explicit repeated statement of the need |
| **Moderate** | 2 independent observations, or 1 observation plus a supporting workflow description |
| **Weak** | 1 observation, or only indirect signals → goes to *Weak signals*, not *Opportunities* |

Repeats within one conversation count as one observation for strength.

## Frequency

Report only what dates support: "5 times between 2026-02-03 and 2026-09-28 (about monthly)". If dates are missing, write "Frequency unknown — 5 occurrences, undated". If the input was sampled, write "at least".

For the at-a-glance table use: **Daily · Weekly · Monthly · Per release / per event · Occasional · Unknown**.

## Cost today

Time and frustration each occurrence costs now, from evidence: stated minutes, number of manual steps, words like "tedious" or "forget", consequences of skipping or mistakes. **High / Medium / Low** with a one-line reason. If the user stated a time ("~20 minutes"), quote it.

## Value

How much the solution would improve things: roughly frequency × cost today, plus consequences of errors it prevents. **High / Medium / Low** with a one-line reason. Do not invent time savings; if you estimate, label it Inferred and show the arithmetic.

## Complexity

Approximate effort for an AI coding agent working with this user:

| Rating | Meaning |
|---|---|
| **XS** | A saved prompt, template, or configuration of an existing tool |
| **S** | Single script, Shortcut, or one-screen app; no persistent data or one local file |
| **M** | Small app with a few screens, local storage, or one external API |
| **L** | Multiple components, sync, background processing, accounts, or platform review |

Add the main risk that could raise complexity (for example "requires App Store Connect API key").

## Privacy considerations

For each opportunity, note:

- What personal or third-party data the solution would touch.
- Whether it can run fully locally.
- Any credentials it would need, and where they should be stored (for example the system keychain, never in source code).

## Redaction

Apply to everything written to the report and briefs:

| Found in input | Write in output |
|---|---|
| API keys, tokens, passwords, private keys | `[REDACTED: API key]` |
| Other people's names, emails, phone numbers, addresses | `[client]`, `[colleague]`, `[email]` |
| Health, financial, or other sensitive details not needed as evidence | Omit or generalize |
| Long passages | A short excerpt (under ~25 words) plus the source reference |

If you find a credential in the input, tell the user in your summary that it exists in their export (without repeating it), because they may want to rotate it.

## The generic-idea test

Ask: *would I suggest this to a random person without reading their material?* If yes, it fails unless the evidence shows a need specific to this person (specific data, specific workflow, specific constraint). Failing ideas are dropped or listed under *Weak signals* with the reason.

## Ranking

Order opportunities by evidence (strength, then number of independent sources), then value, then lower complexity. Do not rank by novelty.
