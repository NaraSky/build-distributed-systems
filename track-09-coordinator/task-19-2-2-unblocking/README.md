# Task 7 - Show How 3PC Unblocks 2PC Scenarios

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-2-unblocking>

Short title: `3PC Unblocking`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-19-2-2-unblocking dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-19-2-2-unblocking\samples\input.jsonl | java -cp '.\track-09-coordinator\task-19-2-2-unblocking\target\classes;.\track-09-coordinator\task-19-2-2-unblocking\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
