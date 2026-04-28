# Task 5 - Implement Log Compaction with Snapshots

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-7-5-snapshots>

Short title: `Snapshots`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-7-5-snapshots dependency:copy-dependencies package
Get-Content .\track-07-store\task-7-5-snapshots\samples\input.jsonl | java -cp '.\track-07-store\task-7-5-snapshots\target\classes;.\track-07-store\task-7-5-snapshots\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
