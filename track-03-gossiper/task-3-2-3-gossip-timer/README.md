# Task 8 - Add Periodic Gossip Rounds on a Timer

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-3-gossip-timer>

Short title: `Gossip Timer`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-2-3-gossip-timer dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-2-3-gossip-timer\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-2-3-gossip-timer\target\classes;.\track-03-gossiper\task-3-2-3-gossip-timer\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
