# Task 9 - Gossip PN-Counter Across a Cluster

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-4-gossip-counter>

Short title: `Gossip Counter`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-17-2-4-gossip-counter dependency:copy-dependencies package
Get-Content .\track-04-counter\task-17-2-4-gossip-counter\samples\input.jsonl | java -cp '.\track-04-counter\task-17-2-4-gossip-counter\target\classes;.\track-04-counter\task-17-2-4-gossip-counter\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
