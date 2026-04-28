# Task 5 - Implement Job Deadlines and Timeouts

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-5-job-deadlines>

Short title: `Deadlines`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-28-orchestrator/task-26-1-5-job-deadlines dependency:copy-dependencies package
Get-Content .\track-28-orchestrator\task-26-1-5-job-deadlines\samples\input.jsonl | java -cp '.\track-28-orchestrator\task-26-1-5-job-deadlines\target\classes;.\track-28-orchestrator\task-26-1-5-job-deadlines\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
