# Evaluations — where the person's project lives

## 2026-10-19 — RED → GREEN → REFACTOR, one cloud LLM

Fresh agent per run, no web search. RED = `build-app` before this change; GREEN = with the *Where your project lives* plan section (plan `schema_version: 2`); REFACTOR = backup asked as a question, with "no backup" as an answer.

| Item | N RED | V RED | N GREEN | V GREEN | N REFACTOR | V REFACTOR |
|---|---|---|---|---|---|---|
| 1 Names the code folder on this computer | ❌ | ✅ `~/Developer/FocusTimer` | ✅ | ✅ | ✅ | ✅ |
| 2 Asks about a backup that fits; "no backup" valid | ❌ | ❌ "you don't need GitHub" | ✅ iCloud Drive or none | ⚠️ assumed a GitHub backup | ✅ | ✅ private GitHub or none |
| 3 Online copy private; public left to `share-app` | n/a | n/a | ✅ | ✅ | ✅ | ✅ |
| 4 Nothing pushed or created online before yes | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 5 Wording fits the level | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**RED:** the newcomer's plan never said where the app's code would live; neither run offered a backup. The developer was told GitHub wasn't needed and nothing would be pushed unless they asked, so the code would stay on one computer.

**GREEN:** both plans named the folder and avoided synced folders (Desktop, Documents, iCloud Drive) on their own. The developer run took "I have a GitHub account" as a yes: it planned a private repository and said approving the plan approved pushing to it.

**REFACTOR:** the plan reference now says to ask the backup as a question, with "no backup" as an answer, and that a mentioned account is not a yes. Both runs then offered the choice, and the plan read "waiting for your answer".

Not tested: the build phase actually creating the private repository or zipped copy; a person with no code host or cloud drive; other LLMs.
