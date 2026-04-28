# Task 4 - Implement Dynamic Mapping with Type Auto-Detection

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-4-dynamic-mapping>

Short title: `Dynamic Mapping`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-23-searcher/task-16-1-4-dynamic-mapping dependency:copy-dependencies package
Get-Content .\track-23-searcher\task-16-1-4-dynamic-mapping\samples\input.jsonl | java -cp '.\track-23-searcher\task-16-1-4-dynamic-mapping\target\classes;.\track-23-searcher\task-16-1-4-dynamic-mapping\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
