# Evaluations — private folder in a git repository

## 2026-10-16 — RED → GREEN, one cloud LLM

Fresh agent per run, no web search. RED = skills as of the CraftApps rename; GREEN = with the "Keep `craftapps/` out of git" step in `build-app` and `discover-app`.

| Item | G RED | D RED | G GREEN | D GREEN |
|---|---|---|---|---|
| 1 Notices the git repository before writing | ⚠️ after writing | ⚠️ after writing | ✅ | ✅ |
| 2 Checks whether `craftapps/` is ignored | ❌ | ❌ | ✅ `git check-ignore` | ✅ `git check-ignore` |
| 3 `git status --short` shows no `craftapps/` | ❌ `?? craftapps/` | ❌ `?? craftapps/` | ✅ clean (`!! craftapps/`) | ✅ clean (`!! craftapps/`) |
| 4 Tells the person plainly | ⚠️ question at the end | ⚠️ warning at the end | ✅ first sentence | ✅ one sentence |
| 5 Tracked files untouched; nothing committed | ✅ | ✅ | ✅ `.git/info/exclude` only | ✅ `.git/info/exclude` only |

**RED:** both left private notes untracked inside the person's repository, one `git add -A` away from being committed and pushed. Both noticed only afterwards and asked the person what to do.

**GREEN:** both checked before writing, used the repository's local exclude file, confirmed the folder was ignored, and told the person in one sentence. The person's `.gitignore` and project files were unchanged; `git status --short` was empty.

Not tested: a repository where `.git/info/exclude` can't be written; git not installed; `share-app` (it writes only into an existing `craftapps/` workspace); other LLMs.
