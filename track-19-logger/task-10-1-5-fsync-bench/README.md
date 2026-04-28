# Task 5 - Benchmark WAL fsync Strategies

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-5-fsync-bench>

Short title: `fsync Benchmark`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-1-5-fsync-bench dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-1-5-fsync-bench\samples\input.jsonl | java -cp '.\track-19-logger\task-10-1-5-fsync-bench\target\classes;.\track-19-logger\task-10-1-5-fsync-bench\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
