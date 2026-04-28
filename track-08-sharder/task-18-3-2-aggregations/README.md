# Task 12 - Implement Cross-Shard Aggregations

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-2-aggregations>

Short title: `Cross-Shard Aggregations`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-18-3-2-aggregations dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-18-3-2-aggregations\samples\input.jsonl | java -cp '.\track-08-sharder\task-18-3-2-aggregations\target\classes;.\track-08-sharder\task-18-3-2-aggregations\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
