# Task 4 - Implement Job Monitoring and Observability

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-4-job-monitoring>

Short title: `Job Monitoring`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-28-orchestrator/task-26-1-4-job-monitoring dependency:copy-dependencies package
Get-Content .\track-28-orchestrator\task-26-1-4-job-monitoring\samples\input.jsonl | java -cp '.\track-28-orchestrator\task-26-1-4-job-monitoring\target\classes;.\track-28-orchestrator\task-26-1-4-job-monitoring\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
