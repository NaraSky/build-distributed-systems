# Task 4 - Implement Saga Pattern

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-4-sagas>

Short title: `Sagas`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-9-4-sagas dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-9-4-sagas\samples\input.jsonl | java -cp '.\track-09-coordinator\task-9-4-sagas\target\classes;.\track-09-coordinator\task-9-4-sagas\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
