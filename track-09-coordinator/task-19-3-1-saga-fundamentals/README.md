# Task 11 - Implement Saga Pattern with Compensating Transactions

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-1-saga-fundamentals>

Short title: `Saga Fundamentals`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-19-3-1-saga-fundamentals dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-19-3-1-saga-fundamentals\samples\input.jsonl | java -cp '.\track-09-coordinator\task-19-3-1-saga-fundamentals\target\classes;.\track-09-coordinator\task-19-3-1-saga-fundamentals\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
