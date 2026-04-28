# Task 2 - Build Flat Tree Topology Gossip

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-tree-topology>

Short title: `Tree Topology`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-2-tree-topology dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-2-tree-topology\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-2-tree-topology\target\classes;.\track-03-gossiper\task-3-2-tree-topology\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
