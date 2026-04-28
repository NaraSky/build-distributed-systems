# Task 8 - Implement Metrics Aggregation and Rollups

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-3-metrics-aggregation>

Short title: `Metrics Aggregation`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-25-tracer/task-23-2-3-metrics-aggregation dependency:copy-dependencies package
Get-Content .\track-25-tracer\task-23-2-3-metrics-aggregation\samples\input.jsonl | java -cp '.\track-25-tracer\task-23-2-3-metrics-aggregation\target\classes;.\track-25-tracer\task-23-2-3-metrics-aggregation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
