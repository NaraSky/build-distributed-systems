# Task 8 - Implement a Multi-Level LSM Tree

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-3-multi-level>

Short title: `Multi-Level LSM`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-2-3-multi-level dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-2-3-multi-level\samples\input.jsonl | java -cp '.\track-19-logger\task-10-2-3-multi-level\target\classes;.\track-19-logger\task-10-2-3-multi-level\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
