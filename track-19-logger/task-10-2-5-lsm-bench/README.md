# Task 10 - Benchmark LSM Tree vs B-Tree Performance

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-5-lsm-bench>

Short title: `LSM Benchmark`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-2-5-lsm-bench dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-2-5-lsm-bench\samples\input.jsonl | java -cp '.\track-19-logger\task-10-2-5-lsm-bench\target\classes;.\track-19-logger\task-10-2-5-lsm-bench\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
