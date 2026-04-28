# Task 18 - Implement Partition Leader Election via Raft

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-3-partition-leader>

Short title: `Partition Leader`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-4-3-partition-leader dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-4-3-partition-leader\samples\input.jsonl | java -cp '.\track-19-logger\task-10-4-3-partition-leader\target\classes;.\track-19-logger\task-10-4-3-partition-leader\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
