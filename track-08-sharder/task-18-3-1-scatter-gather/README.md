# Task 11 - Implement Scatter-Gather Query Execution

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-1-scatter-gather>

Short title: `Scatter-Gather`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-18-3-1-scatter-gather dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-18-3-1-scatter-gather\samples\input.jsonl | java -cp '.\track-08-sharder\task-18-3-1-scatter-gather\target\classes;.\track-08-sharder\task-18-3-1-scatter-gather\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
