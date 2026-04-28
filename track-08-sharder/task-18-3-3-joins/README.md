# Task 13 - Implement Cross-Shard JOINs

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-3-joins>

Short title: `Cross-Shard JOINs`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-18-3-3-joins dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-18-3-3-joins\samples\input.jsonl | java -cp '.\track-08-sharder\task-18-3-3-joins\target\classes;.\track-08-sharder\task-18-3-3-joins\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
