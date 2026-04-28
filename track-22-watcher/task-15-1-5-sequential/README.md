# Task 5 - Implement Sequential Nodes for Ordering

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-5-sequential>

Short title: `Sequential Nodes`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-1-5-sequential dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-1-5-sequential\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-1-5-sequential\target\classes;.\track-22-watcher\task-15-1-5-sequential\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
