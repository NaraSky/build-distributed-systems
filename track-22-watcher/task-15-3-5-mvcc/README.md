# Task 15 - Implement etcd MVCC for Versioned Key-Value Store

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-5-mvcc>

Short title: `etcd MVCC`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-3-5-mvcc dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-3-5-mvcc\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-3-5-mvcc\target\classes;.\track-22-watcher\task-15-3-5-mvcc\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
