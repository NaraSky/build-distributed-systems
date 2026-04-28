# Task 1 - Implement Two-Phase Commit

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-1-two-phase-commit>

Short title: `2PC`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-9-1-two-phase-commit dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-9-1-two-phase-commit\samples\input.jsonl | java -cp '.\track-09-coordinator\task-9-1-two-phase-commit\target\classes;.\track-09-coordinator\task-9-1-two-phase-commit\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
