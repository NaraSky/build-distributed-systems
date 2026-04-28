# Task 9 - Implement Shard Rebalancing on Node Join

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-4-shard-rebalance>

Short title: `Shard Rebalance`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-23-searcher/task-16-2-4-shard-rebalance dependency:copy-dependencies package
Get-Content .\track-23-searcher\task-16-2-4-shard-rebalance\samples\input.jsonl | java -cp '.\track-23-searcher\task-16-2-4-shard-rebalance\target\classes;.\track-23-searcher\task-16-2-4-shard-rebalance\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
