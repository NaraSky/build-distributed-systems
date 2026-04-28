# Task 6 - Implement Chunk Server Heartbeats

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-1-heartbeats>

Short title: `Heartbeats`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-20-filesystem/task-12-2-1-heartbeats dependency:copy-dependencies package
Get-Content .\track-20-filesystem\task-12-2-1-heartbeats\samples\input.jsonl | java -cp '.\track-20-filesystem\task-12-2-1-heartbeats\target\classes;.\track-20-filesystem\task-12-2-1-heartbeats\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
