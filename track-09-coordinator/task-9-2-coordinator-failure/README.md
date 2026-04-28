# Task 2 - Handle Coordinator Failure

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-2-coordinator-failure>

Short title: `Coordinator Failure`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-9-2-coordinator-failure dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-9-2-coordinator-failure\samples\input.jsonl | java -cp '.\track-09-coordinator\task-9-2-coordinator-failure\target\classes;.\track-09-coordinator\task-9-2-coordinator-failure\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
