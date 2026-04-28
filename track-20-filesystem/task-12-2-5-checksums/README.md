# Task 10 - Implement Chunk Checksums for Data Integrity

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-5-checksums>

Short title: `Chunk Checksums`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-20-filesystem/task-12-2-5-checksums dependency:copy-dependencies package
Get-Content .\track-20-filesystem\task-12-2-5-checksums\samples\input.jsonl | java -cp '.\track-20-filesystem\task-12-2-5-checksums\target\classes;.\track-20-filesystem\task-12-2-5-checksums\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
