# Task 7 - Add Virtual Nodes for Even Distribution

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-2-virtual-nodes>

Short title: `Virtual Nodes`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-18-2-2-virtual-nodes dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-18-2-2-virtual-nodes\samples\input.jsonl | java -cp '.\track-08-sharder\task-18-2-2-virtual-nodes\target\classes;.\track-08-sharder\task-18-2-2-virtual-nodes\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
