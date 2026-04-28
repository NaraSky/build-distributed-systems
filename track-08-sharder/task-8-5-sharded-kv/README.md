# Task 5 - Build Complete Sharded Key-Value Store

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-8-5-sharded-kv>

Short title: `Sharded KV`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-8-5-sharded-kv dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-8-5-sharded-kv\samples\input.jsonl | java -cp '.\track-08-sharder\task-8-5-sharded-kv\target\classes;.\track-08-sharder\task-8-5-sharded-kv\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
