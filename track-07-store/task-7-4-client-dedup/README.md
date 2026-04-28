# Task 4 - Handle Client Retry and Deduplication

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-7-4-client-dedup>

Short title: `Client Dedup`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-7-4-client-dedup dependency:copy-dependencies package
Get-Content .\track-07-store\task-7-4-client-dedup\samples\input.jsonl | java -cp '.\track-07-store\task-7-4-client-dedup\target\classes;.\track-07-store\task-7-4-client-dedup\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
