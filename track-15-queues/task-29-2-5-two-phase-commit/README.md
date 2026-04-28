# Task 10 - Implement Two-Phase Commit for Queue and Database

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-5-two-phase-commit>

Short title: `Two-Phase Commit`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-15-queues/task-29-2-5-two-phase-commit dependency:copy-dependencies package
Get-Content .\track-15-queues\task-29-2-5-two-phase-commit\samples\input.jsonl | java -cp '.\track-15-queues\task-29-2-5-two-phase-commit\target\classes;.\track-15-queues\task-29-2-5-two-phase-commit\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
