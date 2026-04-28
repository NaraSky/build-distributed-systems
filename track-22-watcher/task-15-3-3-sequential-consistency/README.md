# Task 13 - Prove ZAB Sequential Consistency

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-3-sequential-consistency>

Short title: `Sequential Consistency`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-3-3-sequential-consistency dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-3-3-sequential-consistency\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-3-3-sequential-consistency\target\classes;.\track-22-watcher\task-15-3-3-sequential-consistency\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
