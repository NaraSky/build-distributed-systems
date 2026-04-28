# Task 8 - Implement Scatter-Gather Search Across Shards

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-3-scatter-gather>

Short title: `Scatter-Gather`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-23-searcher/task-16-2-3-scatter-gather dependency:copy-dependencies package
Get-Content .\track-23-searcher\task-16-2-3-scatter-gather\samples\input.jsonl | java -cp '.\track-23-searcher\task-16-2-3-scatter-gather\target\classes;.\track-23-searcher\task-16-2-3-scatter-gather\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
