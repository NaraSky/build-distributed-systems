# Task 7 - Implement Automatic Re-Replication

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-2-re-replication>

Short title: `Re-Replication`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-20-filesystem/task-12-2-2-re-replication dependency:copy-dependencies package
Get-Content .\track-20-filesystem\task-12-2-2-re-replication\samples\input.jsonl | java -cp '.\track-20-filesystem\task-12-2-2-re-replication\target\classes;.\track-20-filesystem\task-12-2-2-re-replication\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
