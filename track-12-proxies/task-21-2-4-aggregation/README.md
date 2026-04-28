# Task 9 - Implement API Composition and Aggregation

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-4-aggregation>

Short title: `API Composition`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-12-proxies/task-21-2-4-aggregation dependency:copy-dependencies package
Get-Content .\track-12-proxies\task-21-2-4-aggregation\samples\input.jsonl | java -cp '.\track-12-proxies\task-21-2-4-aggregation\target\classes;.\track-12-proxies\task-21-2-4-aggregation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
