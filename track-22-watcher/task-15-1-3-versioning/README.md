# Task 3 - Implement Optimistic Concurrency with Version Checks

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-3-versioning>

Short title: `Version Checks`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-1-3-versioning dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-1-3-versioning\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-1-3-versioning\target\classes;.\track-22-watcher\task-15-1-3-versioning\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
