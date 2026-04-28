# Task 1 - Implement Log Replication

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-6-1-log-replication>

Short title: `Log Replication`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-6-1-log-replication dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-6-1-log-replication\samples\input.jsonl | java -cp '.\track-06-consensus\task-6-1-log-replication\target\classes;.\track-06-consensus\task-6-1-log-replication\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
