# Task 9 - Implement Outbox Pattern

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-4-outbox-pattern>

Short title: `Outbox Pattern`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-15-queues/task-29-2-4-outbox-pattern dependency:copy-dependencies package
Get-Content .\track-15-queues\task-29-2-4-outbox-pattern\samples\input.jsonl | java -cp '.\track-15-queues\task-29-2-4-outbox-pattern\target\classes;.\track-15-queues\task-29-2-4-outbox-pattern\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
