# Task 4 - Implement Exactly-Once Semantics

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-15-4-exactly-once>

Short title: `Exactly-Once`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-15-queues/task-15-4-exactly-once dependency:copy-dependencies package
Get-Content .\track-15-queues\task-15-4-exactly-once\samples\input.jsonl | java -cp '.\track-15-queues\task-15-4-exactly-once\target\classes;.\track-15-queues\task-15-4-exactly-once\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
