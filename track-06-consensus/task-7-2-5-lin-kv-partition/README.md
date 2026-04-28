# Task 10 - Pass Linearizable KV with Network Partitions

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-5-lin-kv-partition>

Short title: `Lin-KV Partitions`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-2-5-lin-kv-partition dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-2-5-lin-kv-partition\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-2-5-lin-kv-partition\target\classes;.\track-06-consensus\task-7-2-5-lin-kv-partition\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
