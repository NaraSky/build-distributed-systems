# Task 8 - Show 3PC Blocking Under Network Partition

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-3-network-partition>

Short title: `3PC Network Partition`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-19-2-3-network-partition dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-19-2-3-network-partition\samples\input.jsonl | java -cp '.\track-09-coordinator\task-19-2-3-network-partition\target\classes;.\track-09-coordinator\task-19-2-3-network-partition\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
