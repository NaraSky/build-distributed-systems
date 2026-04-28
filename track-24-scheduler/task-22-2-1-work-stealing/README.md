# Task 6 - Implement Work Stealing Scheduler

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-1-work-stealing>

Short title: `Work Stealing`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-24-scheduler/task-22-2-1-work-stealing dependency:copy-dependencies package
Get-Content .\track-24-scheduler\task-22-2-1-work-stealing\samples\input.jsonl | java -cp '.\track-24-scheduler\task-22-2-1-work-stealing\target\classes;.\track-24-scheduler\task-22-2-1-work-stealing\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
