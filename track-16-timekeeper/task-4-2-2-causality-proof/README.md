# Task 7 - Prove Lamport Clock Causality and Its Limitation

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-2-causality-proof>

Short title: `Causality Proof`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-2-2-causality-proof dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-2-2-causality-proof\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-2-2-causality-proof\target\classes;.\track-16-timekeeper\task-4-2-2-causality-proof\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
