# Task 4 - Implement Chunk Replication with Pipeline Writes

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-4-chunk-replication>

Short title: `Chunk Replication`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-20-filesystem/task-12-1-4-chunk-replication dependency:copy-dependencies package
Get-Content .\track-20-filesystem\task-12-1-4-chunk-replication\samples\input.jsonl | java -cp '.\track-20-filesystem\task-12-1-4-chunk-replication\target\classes;.\track-20-filesystem\task-12-1-4-chunk-replication\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
