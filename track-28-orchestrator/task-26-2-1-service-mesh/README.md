# Task 6 - Implement Service Mesh Architecture

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-1-service-mesh>

Short title: `Service Mesh`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-28-orchestrator/task-26-2-1-service-mesh dependency:copy-dependencies package
Get-Content .\track-28-orchestrator\task-26-2-1-service-mesh\samples\input.jsonl | java -cp '.\track-28-orchestrator\task-26-2-1-service-mesh\target\classes;.\track-28-orchestrator\task-26-2-1-service-mesh\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
