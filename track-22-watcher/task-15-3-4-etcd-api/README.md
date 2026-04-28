# Task 14 - Implement an etcd-Compatible API Layer

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-4-etcd-api>

Short title: `etcd API`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-3-4-etcd-api dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-3-4-etcd-api\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-3-4-etcd-api\target\classes;.\track-22-watcher\task-15-3-4-etcd-api\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
