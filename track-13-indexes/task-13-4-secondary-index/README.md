# Task 4 - Add Secondary Indexes

Website: <https://builddistributedsystem.com/tracks/indexes/tasks/task-13-4-secondary-index>

Short title: `Secondary Index`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-13-indexes/task-13-4-secondary-index dependency:copy-dependencies package
Get-Content .\track-13-indexes\task-13-4-secondary-index\samples\input.jsonl | java -cp '.\track-13-indexes\task-13-4-secondary-index\target\classes;.\track-13-indexes\task-13-4-secondary-index\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
