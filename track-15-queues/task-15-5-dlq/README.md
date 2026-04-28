# Task 5 - Add Dead Letter Queues

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-15-5-dlq>

Short title: `Dead Letter Queue`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-15-queues/task-15-5-dlq dependency:copy-dependencies package
Get-Content .\track-15-queues\task-15-5-dlq\samples\input.jsonl | java -cp '.\track-15-queues\task-15-5-dlq\target\classes;.\track-15-queues\task-15-5-dlq\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
