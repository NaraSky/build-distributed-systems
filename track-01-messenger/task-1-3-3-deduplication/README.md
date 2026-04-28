# Task 13 - Implement Message Deduplication with LRU Cache

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-3-deduplication>

Short title: `Deduplication`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-3-3-deduplication dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-3-3-deduplication\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-3-3-deduplication\target\classes;.\track-01-messenger\task-1-3-3-deduplication\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
