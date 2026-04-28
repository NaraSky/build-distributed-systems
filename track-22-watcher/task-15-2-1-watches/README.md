# Task 6 - Implement One-Shot Watches for Change Notification

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-1-watches>

Short title: `Watches`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-2-1-watches dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-2-1-watches\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-2-1-watches\target\classes;.\track-22-watcher\task-15-2-1-watches\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
