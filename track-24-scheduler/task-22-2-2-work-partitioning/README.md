# Task 7 - Implement MapReduce-Style Work Partitioning

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-2-work-partitioning>

Short title: `Work Partitioning`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-24-scheduler/task-22-2-2-work-partitioning dependency:copy-dependencies package
Get-Content .\track-24-scheduler\task-22-2-2-work-partitioning\samples\input.jsonl | java -cp '.\track-24-scheduler\task-22-2-2-work-partitioning\target\classes;.\track-24-scheduler\task-22-2-2-work-partitioning\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
