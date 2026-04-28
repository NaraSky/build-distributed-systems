# Task 1 - Implement Shard Controller

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-8-1-shard-controller>

Short title: `Shard Controller`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-8-1-shard-controller dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-8-1-shard-controller\samples\input.jsonl | java -cp '.\track-08-sharder\task-8-1-shard-controller\target\classes;.\track-08-sharder\task-8-1-shard-controller\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
