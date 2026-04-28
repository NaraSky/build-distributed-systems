# Task 8 - Handle Node Addition with Minimal Key Migration

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-3-node-join>

Short title: `Node Join`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-18-2-3-node-join dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-18-2-3-node-join\samples\input.jsonl | java -cp '.\track-08-sharder\task-18-2-3-node-join\target\classes;.\track-08-sharder\task-18-2-3-node-join\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
