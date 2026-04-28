# Task 16 - Implement Grow-Only Set (G-Set) with Gossip

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-1-gset>

Short title: `G-Set`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-4-1-gset dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-4-1-gset\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-4-1-gset\target\classes;.\track-03-gossiper\task-3-4-1-gset\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
