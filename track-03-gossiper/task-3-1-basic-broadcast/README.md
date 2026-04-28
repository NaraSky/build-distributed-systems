# Task 1 - Implement Basic Broadcast to All Nodes

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-1-basic-broadcast>

Short title: `Basic Broadcast`

Difficulty: `beginner`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-1-basic-broadcast dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-1-basic-broadcast\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-1-basic-broadcast\target\classes;.\track-03-gossiper\task-3-1-basic-broadcast\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
