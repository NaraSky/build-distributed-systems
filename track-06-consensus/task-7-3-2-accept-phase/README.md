# Task 12 - Implement Paxos Phase 2 (Accept/Accepted)

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-2-accept-phase>

Short title: `Paxos Phase 2`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-3-2-accept-phase dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-3-2-accept-phase\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-3-2-accept-phase\target\classes;.\track-06-consensus\task-7-3-2-accept-phase\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
