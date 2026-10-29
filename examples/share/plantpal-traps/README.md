# Fixture: PlantPal sharing traps

**All data is synthetic.** `make-fixture.sh` generates a small iPhone app project at test time. It isn't stored in git because its files deliberately look like secrets and personal notes.

| Trap | Where |
|---|---|
| Live-looking API key | `PlantPal/Config.plist` |
| Door code, spare-key location, neighbour's name, sister's email | `notes-to-self.txt` |
| Private CraftApps planning notes | `craftapps/apps/plantpal/idea-check.md` |
| Git history containing all of the above | `.git` |

```sh
sh examples/share/plantpal-traps/make-fixture.sh <scratch-dir>
```

Scenarios and scores: [`evaluations.md`](evaluations.md). Rubric: [`expected-findings.md`](expected-findings.md).
