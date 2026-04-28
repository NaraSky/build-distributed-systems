# Task 2 - Implement WAL Recovery on Startup

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-2-wal-recovery>

Short title: `WAL Recovery`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-1-2-wal-recovery dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-1-2-wal-recovery\samples\input.jsonl | java -cp '.\track-19-logger\task-10-1-2-wal-recovery\target\classes;.\track-19-logger\task-10-1-2-wal-recovery\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
