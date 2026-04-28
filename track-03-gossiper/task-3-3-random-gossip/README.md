# Task 3 - Implement Peer-to-Peer Gossip with Random Neighbors

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-random-gossip>

Short title: `Random Gossip`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-3-random-gossip dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-3-random-gossip\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-3-random-gossip\target\classes;.\track-03-gossiper\task-3-3-random-gossip\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
