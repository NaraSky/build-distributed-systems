# Task 1 - Implement Centralized Job Scheduler

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-1-centralized-scheduler>

Short title: `Centralized Scheduler`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-24-scheduler/task-22-1-1-centralized-scheduler dependency:copy-dependencies package
Get-Content .\track-24-scheduler\task-22-1-1-centralized-scheduler\samples\input.jsonl | java -cp '.\track-24-scheduler\task-22-1-1-centralized-scheduler\target\classes;.\track-24-scheduler\task-22-1-1-centralized-scheduler\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
