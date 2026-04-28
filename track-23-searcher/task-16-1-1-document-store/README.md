# Task 1 - Implement a JSON Document Store

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-1-document-store>

Short title: `Document Store`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-23-searcher/task-16-1-1-document-store dependency:copy-dependencies package
Get-Content .\track-23-searcher\task-16-1-1-document-store\samples\input.jsonl | java -cp '.\track-23-searcher\task-16-1-1-document-store\target\classes;.\track-23-searcher\task-16-1-1-document-store\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
