# Task 4 - Implement WAL Compaction with Atomic Snapshot

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-4-compaction>

Short title: `WAL Compaction`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-1-4-compaction dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-1-4-compaction\samples\input.jsonl | java -cp '.\track-19-logger\task-10-1-4-compaction\target\classes;.\track-19-logger\task-10-1-4-compaction\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
