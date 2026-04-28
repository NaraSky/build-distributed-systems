# Task 3 - Implement Distributed Trace Collector

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-3-trace-collector>

Short title: `Trace Collector`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-25-tracer/task-23-1-3-trace-collector dependency:copy-dependencies package
Get-Content .\track-25-tracer\task-23-1-3-trace-collector\samples\input.jsonl | java -cp '.\track-25-tracer\task-23-1-3-trace-collector\target\classes;.\track-25-tracer\task-23-1-3-trace-collector\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
