# Task 4 - Add Eviction Strategies (LRU, TTL)

Website: <https://builddistributedsystem.com/tracks/caches/tasks/task-11-4-eviction>

Short title: `Eviction`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-11-caches/task-11-4-eviction dependency:copy-dependencies package
Get-Content .\track-11-caches\task-11-4-eviction\samples\input.jsonl | java -cp '.\track-11-caches\task-11-4-eviction\target\classes;.\track-11-caches\task-11-4-eviction\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
