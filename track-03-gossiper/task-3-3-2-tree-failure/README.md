# Task 12 - Handle Tree Node Failure with Direct Fallback

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-2-tree-failure>

Short title: `Tree Failure`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-3-2-tree-failure dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-3-2-tree-failure\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-3-2-tree-failure\target\classes;.\track-03-gossiper\task-3-3-2-tree-failure\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
