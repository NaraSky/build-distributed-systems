# Task 11 - Implement ZAB Atomic Broadcast Protocol

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-1-zab>

Short title: `ZAB Broadcast`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-3-1-zab dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-3-1-zab\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-3-1-zab\target\classes;.\track-22-watcher\task-15-3-1-zab\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
