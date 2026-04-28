# Task 3 - Implement Byzantine Fault Tolerance

Website: <https://builddistributedsystem.com/tracks/advanced/tasks/task-10-3-pbft>

Short title: `PBFT`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-10-advanced/task-10-3-pbft dependency:copy-dependencies package
Get-Content .\track-10-advanced\task-10-3-pbft\samples\input.jsonl | java -cp '.\track-10-advanced\task-10-3-pbft\target\classes;.\track-10-advanced\task-10-3-pbft\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
