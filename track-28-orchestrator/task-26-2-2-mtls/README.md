# Task 7 - Implement mTLS Authentication in Service Mesh

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-2-mtls>

Short title: `mTLS`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-28-orchestrator/task-26-2-2-mtls dependency:copy-dependencies package
Get-Content .\track-28-orchestrator\task-26-2-2-mtls\samples\input.jsonl | java -cp '.\track-28-orchestrator\task-26-2-2-mtls\target\classes;.\track-28-orchestrator\task-26-2-2-mtls\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
