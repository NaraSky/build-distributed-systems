# Task 13 - Implement Orchestration-Based Saga

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-3-orchestration>

Short title: `Orchestration Saga`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-19-3-3-orchestration dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-19-3-3-orchestration\samples\input.jsonl | java -cp '.\track-09-coordinator\task-19-3-3-orchestration\target\classes;.\track-09-coordinator\task-19-3-3-orchestration\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
