# Task 3 - Implement At-Least-Once Delivery

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-15-3-at-least-once>

Short title: `At-Least-Once`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-15-queues/task-15-3-at-least-once dependency:copy-dependencies package
Get-Content .\track-15-queues\task-15-3-at-least-once\samples\input.jsonl | java -cp '.\track-15-queues\task-15-3-at-least-once\target\classes;.\track-15-queues\task-15-3-at-least-once\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
