# Task 14 - Benchmark Node Throughput and Latency

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-4-throughput-bench>

Short title: `Throughput Bench`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-3-4-throughput-bench dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-3-4-throughput-bench\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-3-4-throughput-bench\target\classes;.\track-01-messenger\task-1-3-4-throughput-bench\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
