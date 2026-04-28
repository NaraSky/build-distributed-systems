# Task 5 - Build Transactional Key-Value Store

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-5-txn-kv>

Short title: `Txn KV`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-9-5-txn-kv dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-9-5-txn-kv\samples\input.jsonl | java -cp '.\track-09-coordinator\task-9-5-txn-kv\target\classes;.\track-09-coordinator\task-9-5-txn-kv\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
