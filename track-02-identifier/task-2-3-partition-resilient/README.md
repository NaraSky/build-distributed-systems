# Task 3 - Implement ID Generation During Network Partition

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-partition-resilient>

Short title: `Partition Resilient`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-3-partition-resilient dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-3-partition-resilient\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-3-partition-resilient\target\classes;.\track-02-identifier\task-2-3-partition-resilient\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
