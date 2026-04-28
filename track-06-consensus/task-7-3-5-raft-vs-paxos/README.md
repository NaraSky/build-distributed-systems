# Task 15 - Compare Raft vs Multi-Paxos

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-5-raft-vs-paxos>

Short title: `Raft vs Paxos`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-3-5-raft-vs-paxos dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-3-5-raft-vs-paxos\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-3-5-raft-vs-paxos\target\classes;.\track-06-consensus\task-7-3-5-raft-vs-paxos\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
