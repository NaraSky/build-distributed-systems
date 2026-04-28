# Task 10 - Implement Alert Integrations and On-Call Management

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-5-alert-integrations>

Short title: `Alert Integrations`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-25-tracer/task-23-2-5-alert-integrations dependency:copy-dependencies package
Get-Content .\track-25-tracer\task-23-2-5-alert-integrations\samples\input.jsonl | java -cp '.\track-25-tracer\task-23-2-5-alert-integrations\target\classes;.\track-25-tracer\task-23-2-5-alert-integrations\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
