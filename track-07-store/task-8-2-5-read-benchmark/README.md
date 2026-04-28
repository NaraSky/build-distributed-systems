# Task 10 - Benchmark Read Strategies Under Mixed Workload

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-2-5-read-benchmark>

Short title: `Read Benchmark`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-8-2-5-read-benchmark dependency:copy-dependencies package
Get-Content .\track-07-store\task-8-2-5-read-benchmark\samples\input.jsonl | java -cp '.\track-07-store\task-8-2-5-read-benchmark\target\classes;.\track-07-store\task-8-2-5-read-benchmark\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
