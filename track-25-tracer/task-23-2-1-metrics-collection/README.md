# Task 6 - Implement Metrics Collection

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-1-metrics-collection>

Short title: `Metrics Collection`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-25-tracer/task-23-2-1-metrics-collection dependency:copy-dependencies package
Get-Content .\track-25-tracer\task-23-2-1-metrics-collection\samples\input.jsonl | java -cp '.\track-25-tracer\task-23-2-1-metrics-collection\target\classes;.\track-25-tracer\task-23-2-1-metrics-collection\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
