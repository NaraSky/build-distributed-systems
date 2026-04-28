# Task 7 - Implement Idempotent Consumers

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-2-idempotent-consumers>

Short title: `Idempotent Consumers`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-15-queues/task-29-2-2-idempotent-consumers dependency:copy-dependencies package
Get-Content .\track-15-queues\task-29-2-2-idempotent-consumers\samples\input.jsonl | java -cp '.\track-15-queues\task-29-2-2-idempotent-consumers\target\classes;.\track-15-queues\task-29-2-2-idempotent-consumers\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
