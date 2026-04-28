# Task 7 - Add Replica Shards for Fault Tolerance

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-2-replica-shards>

Short title: `Replica Shards`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-23-searcher/task-16-2-2-replica-shards dependency:copy-dependencies package
Get-Content .\track-23-searcher\task-16-2-2-replica-shards\samples\input.jsonl | java -cp '.\track-23-searcher\task-16-2-2-replica-shards\target\classes;.\track-23-searcher\task-16-2-2-replica-shards\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
