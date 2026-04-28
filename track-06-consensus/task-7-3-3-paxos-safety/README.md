# Task 13 - Prove Paxos Safety: Chosen Values Are Immutable

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-3-paxos-safety>

Short title: `Paxos Safety`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-3-3-paxos-safety dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-3-3-paxos-safety\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-3-3-paxos-safety\target\classes;.\track-06-consensus\task-7-3-3-paxos-safety\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
