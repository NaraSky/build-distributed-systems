# Task 11 - Implement Tree-Based Broadcast Overlay

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-1-tree-broadcast>

Short title: `Tree Broadcast`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-3-1-tree-broadcast dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-3-1-tree-broadcast\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-3-1-tree-broadcast\target\classes;.\track-03-gossiper\task-3-3-1-tree-broadcast\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
