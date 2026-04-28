# Task 5 - Implement End-to-End Distributed Tracing System

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-5-distributed-tracing>

Short title: `End-to-End Tracing`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-25-tracer/task-23-1-5-distributed-tracing dependency:copy-dependencies package
Get-Content .\track-25-tracer\task-23-1-5-distributed-tracing\samples\input.jsonl | java -cp '.\track-25-tracer\task-23-1-5-distributed-tracing\target\classes;.\track-25-tracer\task-23-1-5-distributed-tracing\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
