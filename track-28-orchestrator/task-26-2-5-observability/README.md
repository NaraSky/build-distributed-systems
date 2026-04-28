# Task 10 - Implement Service Mesh Observability

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-5-observability>

Short title: `Observability`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-28-orchestrator/task-26-2-5-observability dependency:copy-dependencies package
Get-Content .\track-28-orchestrator\task-26-2-5-observability\samples\input.jsonl | java -cp '.\track-28-orchestrator\task-26-2-5-observability\target\classes;.\track-28-orchestrator\task-26-2-5-observability\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
