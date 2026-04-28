# Task 3 - Implement Three-Phase Commit

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-3-three-phase-commit>

Short title: `3PC`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-9-3-three-phase-commit dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-9-3-three-phase-commit\samples\input.jsonl | java -cp '.\track-09-coordinator\task-9-3-three-phase-commit\target\classes;.\track-09-coordinator\task-9-3-three-phase-commit\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
