# Task 8 - Implement Chunk Server Load Balancing

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-3-load-balancing>

Short title: `Load Balancing`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-20-filesystem/task-12-2-3-load-balancing dependency:copy-dependencies package
Get-Content .\track-20-filesystem\task-12-2-3-load-balancing\samples\input.jsonl | java -cp '.\track-20-filesystem\task-12-2-3-load-balancing\target\classes;.\track-20-filesystem\task-12-2-3-load-balancing\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
