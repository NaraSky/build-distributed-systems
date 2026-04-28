# Task 1 - Implement Distributed Trace Context Propagation

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-1-trace-context-propagation>

Short title: `Trace Propagation`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-25-tracer/task-23-1-1-trace-context-propagation dependency:copy-dependencies package
Get-Content .\track-25-tracer\task-23-1-1-trace-context-propagation\samples\input.jsonl | java -cp '.\track-25-tracer\task-23-1-1-trace-context-propagation\target\classes;.\track-25-tracer\task-23-1-1-trace-context-propagation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
