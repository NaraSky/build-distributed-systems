# Task 14 - Implement Idempotency in Sagas

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-4-idempotency>

Short title: `Saga Idempotency`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-19-3-4-idempotency dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-19-3-4-idempotency\samples\input.jsonl | java -cp '.\track-09-coordinator\task-19-3-4-idempotency\target\classes;.\track-09-coordinator\task-19-3-4-idempotency\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
