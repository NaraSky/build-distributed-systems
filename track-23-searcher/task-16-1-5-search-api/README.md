# Task 5 - Implement a Full-Text Search API

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-5-search-api>

Short title: `Search API`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-23-searcher/task-16-1-5-search-api dependency:copy-dependencies package
Get-Content .\track-23-searcher\task-16-1-5-search-api\samples\input.jsonl | java -cp '.\track-23-searcher\task-16-1-5-search-api\target\classes;.\track-23-searcher\task-16-1-5-search-api\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
