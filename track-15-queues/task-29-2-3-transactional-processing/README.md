# Task 8 - Implement Transactional Message Processing

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-3-transactional-processing>

Short title: `Transactional Processing`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-15-queues/task-29-2-3-transactional-processing dependency:copy-dependencies package
Get-Content .\track-15-queues\task-29-2-3-transactional-processing\samples\input.jsonl | java -cp '.\track-15-queues\task-29-2-3-transactional-processing\target\classes;.\track-15-queues\task-29-2-3-transactional-processing\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
