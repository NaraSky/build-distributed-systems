# Task 10 - Implement Paxos Commit Protocol

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-5-paxos-commit>

Short title: `Paxos Commit`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-19-2-5-paxos-commit dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-19-2-5-paxos-commit\samples\input.jsonl | java -cp '.\track-09-coordinator\task-19-2-5-paxos-commit\target\classes;.\track-09-coordinator\task-19-2-5-paxos-commit\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
