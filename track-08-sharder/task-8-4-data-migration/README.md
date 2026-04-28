# Task 4 - Implement Data Migration

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-8-4-data-migration>

Short title: `Data Migration`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-8-4-data-migration dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-8-4-data-migration\samples\input.jsonl | java -cp '.\track-08-sharder\task-8-4-data-migration\target\classes;.\track-08-sharder\task-8-4-data-migration\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
