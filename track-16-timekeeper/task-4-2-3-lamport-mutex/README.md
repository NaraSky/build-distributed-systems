# Task 8 - Implement Distributed Mutual Exclusion with Lamport Clocks

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-3-lamport-mutex>

Short title: `Lamport Mutex`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-2-3-lamport-mutex dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-2-3-lamport-mutex\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-2-3-lamport-mutex\target\classes;.\track-16-timekeeper\task-4-2-3-lamport-mutex\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
