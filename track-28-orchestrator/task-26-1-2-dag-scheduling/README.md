# Task 2 - Implement DAG-Based Task Scheduling

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-2-dag-scheduling>

Short title: `DAG Scheduling`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-28-orchestrator/task-26-1-2-dag-scheduling dependency:copy-dependencies package
Get-Content .\track-28-orchestrator\task-26-1-2-dag-scheduling\samples\input.jsonl | java -cp '.\track-28-orchestrator\task-26-1-2-dag-scheduling\target\classes;.\track-28-orchestrator\task-26-1-2-dag-scheduling\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
