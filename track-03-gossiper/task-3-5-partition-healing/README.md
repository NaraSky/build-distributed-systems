# Task 5 - Handle Network Partition Healing and Resynchronization

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-5-partition-healing>

Short title: `Partition Healing`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-5-partition-healing dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-5-partition-healing\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-5-partition-healing\target\classes;.\track-03-gossiper\task-3-5-partition-healing\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
