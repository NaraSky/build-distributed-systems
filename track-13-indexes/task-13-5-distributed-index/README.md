# Task 5 - Distribute Index Across Nodes

Website: <https://builddistributedsystem.com/tracks/indexes/tasks/task-13-5-distributed-index>

Short title: `Distributed Index`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-13-indexes/task-13-5-distributed-index dependency:copy-dependencies package
Get-Content .\track-13-indexes\task-13-5-distributed-index\samples\input.jsonl | java -cp '.\track-13-indexes\task-13-5-distributed-index\target\classes;.\track-13-indexes\task-13-5-distributed-index\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
