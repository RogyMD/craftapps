# Templates

## Review record (private — for the maintainer)

````markdown
---
craftapps_artifact: library-review
schema_version: 1
produced_by: curate-app
created: YYYY-MM-DD
status: draft            # approved only on the maintainer's explicit yes
submission: <app name>
link: <public link as submitted>
reviewed_version: <commit hash, or SHA-256 of the archive>
verdict: approve | changes-requested | reject
build: not verified | verified in sandbox (<what/where>)
---

# Review: <app name>

## Findings

| Severity | File | Finding |
|---|---|---|

## Notes for the maintainer
<!-- Anything the maintainer should decide or know. -->
````

## Library entry (public — approve only)

Public information only. **No email addresses**, no private details, nothing the submitter didn't publish themselves.

````markdown
---
craftapps_artifact: library-entry
schema_version: 1
produced_by: curate-app
created: YYYY-MM-DD
status: draft            # approved only on the maintainer's explicit yes
name: <app name>
platforms: [<e.g. macOS 14+>]
license: <SPDX id, e.g. MIT>
link: <public link>
reviewed_version: <commit hash or archive SHA-256>
---

# <App name>

<One or two sentences: the problem it solves, in plain language.>

- **Platforms:** …
- **Your data:** <e.g. "stays on your Mac; no network, no account">
- **License:** …
- **Made by:** <public name or handle as shown at the link>
- **Get it:** <link> (reviewed version: <short hash>)
- **Status:** <the submitter's own status line>
- **Known limitations:** <Low findings worth knowing, or "none noted">

Reviewed by CraftApps on YYYY-MM-DD: source read in full; build <not verified | verified in a sandbox>. Reviews reduce risk but are not a guarantee.
````

## Reply to the submitter (draft — the maintainer sends it)

Kind, specific, short. Thank them for making and sharing it.

- **Approve:** it's listed (after the maintainer publishes); link to the entry; any Low notes as friendly suggestions.
- **Changes requested:** what to change and why, in plain language; invite them to resubmit.
- **Reject:** the reason, factually and without accusation, for example "the app sends notes to an external server, which the README says it doesn't". Mention anything they should fix for their own users' safety. Never include exploit details.
- If their submission contained a secret: tell them to revoke it.

```
To: <submitter address from the email>
From: craft.apps@aigarden.uk
Subject: Re: CraftApps library submission: <app name>

<body>
```
