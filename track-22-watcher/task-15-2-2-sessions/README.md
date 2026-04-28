# Task 7 - Implement Client Session Management

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-2-sessions>

Short title: `Sessions`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-2-2-sessions dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-2-2-sessions\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-2-2-sessions\target\classes;.\track-22-watcher\task-15-2-2-sessions\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
