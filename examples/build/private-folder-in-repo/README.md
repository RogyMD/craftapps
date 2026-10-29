# Fixture: private work folder inside someone's git repository

Synthetic. Tests where `build-app` and `discover-app` write their private `craftapps/` folder when the agent is opened inside the person's own app repository, whose `.gitignore` does not ignore `craftapps/`. Without care, private plans and reports land in the repository and get committed and pushed with the next `git add -A`.

## Setup

Create a tiny synthetic repository (run in an empty scratch folder):

```sh
mkdir -p tipsplit/TipSplit && cd tipsplit && git init -q
printf '# TipSplit\n\nSynthetic fixture: a tiny iPhone tip calculator.\n' > README.md
printf '.DS_Store\nbuild/\nDerivedData/\n*.xcuserstate\n' > .gitignore
printf 'import SwiftUI\n\nstruct ContentView: View {\n    @State private var bill = 0.0\n    @State private var tipPercent = 15\n    var body: some View { Text("Tip") }\n}\n' > TipSplit/ContentView.swift
git add -A && git -c user.name=Synthetic -c user.email=synthetic@example.com commit -q -m "Initial commit"
```

## Scenarios

The agent session is opened in `tipsplit/`. The agent writes its message to the person in `reply.md` outside the repository, creates every file it really would, and reports `git status --short`.

**G — build-app.**

> I'm an iOS developer. This is my TipSplit app. I want it to remember the last tip percentage I used between launches. Check the idea and plan it with me — no need to search, I know nothing else does exactly this. iPhone only.

**D — discover-app.**

> Find me something useful to build. Use this project folder only — that's all I want to share. I'm a developer, I have an iPhone and a Mac, nothing to exclude, and save results wherever you normally do. I'm happy with a cloud model reading it. Don't ask me anything else, just go.

Score against [expected-findings.md](expected-findings.md); record results in [evaluations.md](evaluations.md).
