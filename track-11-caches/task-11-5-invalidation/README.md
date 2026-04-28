# Task 5 - Handle Cache Invalidation and Consistency

Website: <https://builddistributedsystem.com/tracks/caches/tasks/task-11-5-invalidation>

Short title: `Invalidation`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-11-caches/task-11-5-invalidation dependency:copy-dependencies package
Get-Content .\track-11-caches\task-11-5-invalidation\samples\input.jsonl | java -cp '.\track-11-caches\task-11-5-invalidation\target\classes;.\track-11-caches\task-11-5-invalidation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
