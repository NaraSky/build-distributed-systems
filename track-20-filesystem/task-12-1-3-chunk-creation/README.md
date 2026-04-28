# Task 3 - Implement Chunk Creation and Allocation

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-3-chunk-creation>

Short title: `Chunk Creation`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-20-filesystem/task-12-1-3-chunk-creation dependency:copy-dependencies package
Get-Content .\track-20-filesystem\task-12-1-3-chunk-creation\samples\input.jsonl | java -cp '.\track-20-filesystem\task-12-1-3-chunk-creation\target\classes;.\track-20-filesystem\task-12-1-3-chunk-creation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
