# Task 2 - Implement Schema Mapping with Field Types

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-2-schema-mapping>

Short title: `Schema Mapping`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-23-searcher/task-16-1-2-schema-mapping dependency:copy-dependencies package
Get-Content .\track-23-searcher\task-16-1-2-schema-mapping\samples\input.jsonl | java -cp '.\track-23-searcher\task-16-1-2-schema-mapping\target\classes;.\track-23-searcher\task-16-1-2-schema-mapping\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
