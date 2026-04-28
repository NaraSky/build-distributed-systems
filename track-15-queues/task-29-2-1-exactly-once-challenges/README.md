# Task 6 - Understand Exactly-Once Delivery Challenges

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-1-exactly-once-challenges>

Short title: `Exactly-Once Challenges`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-15-queues/task-29-2-1-exactly-once-challenges dependency:copy-dependencies package
Get-Content .\track-15-queues\task-29-2-1-exactly-once-challenges\samples\input.jsonl | java -cp '.\track-15-queues\task-29-2-1-exactly-once-challenges\target\classes;.\track-15-queues\task-29-2-1-exactly-once-challenges\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
