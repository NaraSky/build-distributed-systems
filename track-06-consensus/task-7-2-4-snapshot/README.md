# Task 9 - Add Snapshot Support for Log Compaction

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-4-snapshot>

Short title: `Snapshots`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-2-4-snapshot dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-2-4-snapshot\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-2-4-snapshot\target\classes;.\track-06-consensus\task-7-2-4-snapshot\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
