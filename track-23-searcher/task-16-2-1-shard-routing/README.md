# Task 6 - Implement Document Sharding with Hash-Based Routing

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-1-shard-routing>

Short title: `Shard Routing`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-23-searcher/task-16-2-1-shard-routing dependency:copy-dependencies package
Get-Content .\track-23-searcher\task-16-2-1-shard-routing\samples\input.jsonl | java -cp '.\track-23-searcher\task-16-2-1-shard-routing\target\classes;.\track-23-searcher\task-16-2-1-shard-routing\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
