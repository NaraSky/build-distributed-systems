# Task 1 - Implement a Write-Ahead Log

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-1-wal-impl>

Short title: `WAL Implementation`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-1-1-wal-impl dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-1-1-wal-impl\samples\input.jsonl | java -cp '.\track-19-logger\task-10-1-1-wal-impl\target\classes;.\track-19-logger\task-10-1-1-wal-impl\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
