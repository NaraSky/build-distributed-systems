# Task 14 - Implement Secondary Indexes on Sharded Data

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-4-secondary-indexes>

Short title: `Secondary Indexes`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-18-3-4-secondary-indexes dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-18-3-4-secondary-indexes\samples\input.jsonl | java -cp '.\track-08-sharder\task-18-3-4-secondary-indexes\target\classes;.\track-08-sharder\task-18-3-4-secondary-indexes\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
