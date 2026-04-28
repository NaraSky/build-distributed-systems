# Task 15 - Simulate Network Partition and Healing

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-5-partition-heal>

Short title: `Partition Heal`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-3-5-partition-heal dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-3-5-partition-heal\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-3-5-partition-heal\target\classes;.\track-03-gossiper\task-3-3-5-partition-heal\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
