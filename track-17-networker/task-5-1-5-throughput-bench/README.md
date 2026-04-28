# Task 5 - Benchmark Server Throughput and Latency

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-5-throughput-bench>

Short title: `Throughput Benchmark`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-1-5-throughput-bench dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-1-5-throughput-bench\samples\input.jsonl | java -cp '.\track-17-networker\task-5-1-5-throughput-bench\target\classes;.\track-17-networker\task-5-1-5-throughput-bench\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
