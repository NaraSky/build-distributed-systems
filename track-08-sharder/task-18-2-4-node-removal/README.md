# Task 9 - Handle Node Removal with Graceful and Crash Recovery

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-4-node-removal>

Short title: `Node Removal`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-18-2-4-node-removal dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-18-2-4-node-removal\samples\input.jsonl | java -cp '.\track-08-sharder\task-18-2-4-node-removal\target\classes;.\track-08-sharder\task-18-2-4-node-removal\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
