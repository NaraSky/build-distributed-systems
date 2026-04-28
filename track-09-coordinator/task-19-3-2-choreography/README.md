# Task 12 - Implement Choreography-Based Saga

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-2-choreography>

Short title: `Choreography Saga`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-19-3-2-choreography dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-19-3-2-choreography\samples\input.jsonl | java -cp '.\track-09-coordinator\task-19-3-2-choreography\target\classes;.\track-09-coordinator\task-19-3-2-choreography\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
