# Task 3 - Implement Resource Management for Jobs

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-3-resource-management>

Short title: `Resource Management`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-28-orchestrator/task-26-1-3-resource-management dependency:copy-dependencies package
Get-Content .\track-28-orchestrator\task-26-1-3-resource-management\samples\input.jsonl | java -cp '.\track-28-orchestrator\task-26-1-3-resource-management\target\classes;.\track-28-orchestrator\task-26-1-3-resource-management\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
