# Task 14 - Implement Multi-Paxos for an Infinite Log

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-4-multi-paxos>

Short title: `Multi-Paxos`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-3-4-multi-paxos dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-3-4-multi-paxos\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-3-4-multi-paxos\target\classes;.\track-06-consensus\task-7-3-4-multi-paxos\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
