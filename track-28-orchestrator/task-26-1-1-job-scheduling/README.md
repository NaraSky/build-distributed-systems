# Task 1 - Implement Job Scheduling System

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-1-job-scheduling>

Short title: `Job Scheduling`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-28-orchestrator/task-26-1-1-job-scheduling dependency:copy-dependencies package
Get-Content .\track-28-orchestrator\task-26-1-1-job-scheduling\samples\input.jsonl | java -cp '.\track-28-orchestrator\task-26-1-1-job-scheduling\target\classes;.\track-28-orchestrator\task-26-1-1-job-scheduling\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
