# Task 8 - Implement Traffic Splitting in Service Mesh

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-3-traffic-splitting>

Short title: `Traffic Splitting`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-28-orchestrator/task-26-2-3-traffic-splitting dependency:copy-dependencies package
Get-Content .\track-28-orchestrator\task-26-2-3-traffic-splitting\samples\input.jsonl | java -cp '.\track-28-orchestrator\task-26-2-3-traffic-splitting\target\classes;.\track-28-orchestrator\task-26-2-3-traffic-splitting\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
