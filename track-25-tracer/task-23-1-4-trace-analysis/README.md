# Task 4 - Implement Trace Analysis and Insights

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-4-trace-analysis>

Short title: `Trace Analysis`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-25-tracer/task-23-1-4-trace-analysis dependency:copy-dependencies package
Get-Content .\track-25-tracer\task-23-1-4-trace-analysis\samples\input.jsonl | java -cp '.\track-25-tracer\task-23-1-4-trace-analysis\target\classes;.\track-25-tracer\task-23-1-4-trace-analysis\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
