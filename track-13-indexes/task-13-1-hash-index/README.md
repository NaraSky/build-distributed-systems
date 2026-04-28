# Task 1 - Implement Hash Index

Website: <https://builddistributedsystem.com/tracks/indexes/tasks/task-13-1-hash-index>

Short title: `Hash Index`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-13-indexes/task-13-1-hash-index dependency:copy-dependencies package
Get-Content .\track-13-indexes\task-13-1-hash-index\samples\input.jsonl | java -cp '.\track-13-indexes\task-13-1-hash-index\target\classes;.\track-13-indexes\task-13-1-hash-index\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
