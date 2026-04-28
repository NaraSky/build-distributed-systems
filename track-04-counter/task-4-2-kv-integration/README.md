# Task 2 - Integrate Sequentially Consistent Key-Value Store

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-4-2-kv-integration>

Short title: `KV Integration`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-4-2-kv-integration dependency:copy-dependencies package
Get-Content .\track-04-counter\task-4-2-kv-integration\samples\input.jsonl | java -cp '.\track-04-counter\task-4-2-kv-integration\target\classes;.\track-04-counter\task-4-2-kv-integration\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
