# Task 14 - Implement a Buffer Pool with LRU Eviction

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-4-buffer-pool>

Short title: `Buffer Pool`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-3-4-buffer-pool dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-3-4-buffer-pool\samples\input.jsonl | java -cp '.\track-19-logger\task-10-3-4-buffer-pool\target\classes;.\track-19-logger\task-10-3-4-buffer-pool\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
