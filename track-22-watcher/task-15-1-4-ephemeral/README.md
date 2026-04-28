# Task 4 - Implement Ephemeral Nodes for Session-Bound State

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-4-ephemeral>

Short title: `Ephemeral Nodes`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-1-4-ephemeral dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-1-4-ephemeral\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-1-4-ephemeral\target\classes;.\track-22-watcher\task-15-1-4-ephemeral\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
