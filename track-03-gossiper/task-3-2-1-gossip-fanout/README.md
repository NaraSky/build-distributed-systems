# Task 6 - Implement Gossip Fanout with Random Peer Selection

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-1-gossip-fanout>

Short title: `Gossip Fanout`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-2-1-gossip-fanout dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-2-1-gossip-fanout\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-2-1-gossip-fanout\target\classes;.\track-03-gossiper\task-3-2-1-gossip-fanout\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
