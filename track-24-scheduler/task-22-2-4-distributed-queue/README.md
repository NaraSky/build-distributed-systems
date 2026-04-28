# Task 9 - Implement Distributed Job Queue

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-4-distributed-queue>

Short title: `Distributed Queue`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-24-scheduler/task-22-2-4-distributed-queue dependency:copy-dependencies package
Get-Content .\track-24-scheduler\task-22-2-4-distributed-queue\samples\input.jsonl | java -cp '.\track-24-scheduler\task-22-2-4-distributed-queue\target\classes;.\track-24-scheduler\task-22-2-4-distributed-queue\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
