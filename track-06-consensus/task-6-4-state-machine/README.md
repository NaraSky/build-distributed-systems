# Task 4 - Apply Committed Entries to State Machine

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-6-4-state-machine>

Short title: `State Machine`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-6-4-state-machine dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-6-4-state-machine\samples\input.jsonl | java -cp '.\track-06-consensus\task-6-4-state-machine\target\classes;.\track-06-consensus\task-6-4-state-machine\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
