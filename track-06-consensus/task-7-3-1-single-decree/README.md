# Task 11 - Implement Single-Decree Paxos Phase 1 (Prepare/Promise)

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-1-single-decree>

Short title: `Paxos Phase 1`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-3-1-single-decree dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-3-1-single-decree\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-3-1-single-decree\target\classes;.\track-06-consensus\task-7-3-1-single-decree\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
