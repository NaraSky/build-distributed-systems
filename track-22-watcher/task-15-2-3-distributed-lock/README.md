# Task 8 - Build a Distributed Lock with ZooKeeper Primitives

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-3-distributed-lock>

Short title: `Distributed Lock`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-2-3-distributed-lock dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-2-3-distributed-lock\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-2-3-distributed-lock\target\classes;.\track-22-watcher\task-15-2-3-distributed-lock\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
