# Task 17 - Prove HLC Preserves Causality Within Epsilon

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-2-hlc-causality-bound>

Short title: `HLC Causality Bound`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-4-2-hlc-causality-bound dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-4-2-hlc-causality-bound\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-4-2-hlc-causality-bound\target\classes;.\track-16-timekeeper\task-4-4-2-hlc-causality-bound\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
