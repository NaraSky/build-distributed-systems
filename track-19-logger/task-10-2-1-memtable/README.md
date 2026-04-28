# Task 6 - Implement an In-Memory MemTable

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-1-memtable>

Short title: `MemTable`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-2-1-memtable dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-2-1-memtable\samples\input.jsonl | java -cp '.\track-19-logger\task-10-2-1-memtable\target\classes;.\track-19-logger\task-10-2-1-memtable\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
