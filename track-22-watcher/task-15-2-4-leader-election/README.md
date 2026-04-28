# Task 9 - Build Leader Election with ZooKeeper

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-4-leader-election>

Short title: `Leader Election`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-2-4-leader-election dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-2-4-leader-election\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-2-4-leader-election\target\classes;.\track-22-watcher\task-15-2-4-leader-election\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
