# Task 8 - Implement Fault-Tolerant Scheduler

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-3-scheduler-fault-tolerance>

Short title: `Fault Tolerance`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-24-scheduler/task-22-2-3-scheduler-fault-tolerance dependency:copy-dependencies package
Get-Content .\track-24-scheduler\task-22-2-3-scheduler-fault-tolerance\samples\input.jsonl | java -cp '.\track-24-scheduler\task-22-2-3-scheduler-fault-tolerance\target\classes;.\track-24-scheduler\task-22-2-3-scheduler-fault-tolerance\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
