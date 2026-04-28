# Task 2 - Add Consumer Groups with Partitions

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-15-2-consumer-groups>

Short title: `Consumer Groups`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-15-queues/task-15-2-consumer-groups dependency:copy-dependencies package
Get-Content .\track-15-queues\task-15-2-consumer-groups\samples\input.jsonl | java -cp '.\track-15-queues\task-15-2-consumer-groups\target\classes;.\track-15-queues\task-15-2-consumer-groups\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
