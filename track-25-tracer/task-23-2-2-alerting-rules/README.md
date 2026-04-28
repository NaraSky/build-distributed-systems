# Task 7 - Implement Alerting Rules Engine

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-2-alerting-rules>

Short title: `Alerting Rules`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-25-tracer/task-23-2-2-alerting-rules dependency:copy-dependencies package
Get-Content .\track-25-tracer\task-23-2-2-alerting-rules\samples\input.jsonl | java -cp '.\track-25-tracer\task-23-2-2-alerting-rules\target\classes;.\track-25-tracer\task-23-2-2-alerting-rules\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
