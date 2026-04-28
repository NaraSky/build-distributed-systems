# Task 1 - Implement Basic Message Queue

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-15-1-basic-queue>

Short title: `Basic Queue`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-15-queues/task-15-1-basic-queue dependency:copy-dependencies package
Get-Content .\track-15-queues\task-15-1-basic-queue\samples\input.jsonl | java -cp '.\track-15-queues\task-15-1-basic-queue\target\classes;.\track-15-queues\task-15-1-basic-queue\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
