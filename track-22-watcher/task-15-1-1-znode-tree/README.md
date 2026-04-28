# Task 1 - Implement a ZNode Tree Data Model

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-1-znode-tree>

Short title: `ZNode Tree`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-1-1-znode-tree dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-1-1-znode-tree\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-1-1-znode-tree\target\classes;.\track-22-watcher\task-15-1-1-znode-tree\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
