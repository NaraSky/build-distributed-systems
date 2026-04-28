# Task 2 - Implement Span Lifecycle Management

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-2-span-lifecycle>

Short title: `Span Lifecycle`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-25-tracer/task-23-1-2-span-lifecycle dependency:copy-dependencies package
Get-Content .\track-25-tracer\task-23-1-2-span-lifecycle\samples\input.jsonl | java -cp '.\track-25-tracer\task-23-1-2-span-lifecycle\target\classes;.\track-25-tracer\task-23-1-2-span-lifecycle\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
