# Task 9 - Implement Circuit Breaking in Service Mesh

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-4-circuit-breaking>

Short title: `Circuit Breaking`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-28-orchestrator/task-26-2-4-circuit-breaking dependency:copy-dependencies package
Get-Content .\track-28-orchestrator\task-26-2-4-circuit-breaking\samples\input.jsonl | java -cp '.\track-28-orchestrator\task-26-2-4-circuit-breaking\target\classes;.\track-28-orchestrator\task-26-2-4-circuit-breaking\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
