# Task 2 - Implement ZNode CRUD Operations

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-2-crud>

Short title: `ZNode CRUD`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-1-2-crud dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-1-2-crud\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-1-2-crud\target\classes;.\track-22-watcher\task-15-1-2-crud\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
