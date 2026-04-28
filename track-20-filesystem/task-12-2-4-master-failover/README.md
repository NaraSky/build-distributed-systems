# Task 9 - Implement Master Failover with Shadow Master

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-4-master-failover>

Short title: `Master Failover`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-20-filesystem/task-12-2-4-master-failover dependency:copy-dependencies package
Get-Content .\track-20-filesystem\task-12-2-4-master-failover\samples\input.jsonl | java -cp '.\track-20-filesystem\task-12-2-4-master-failover\target\classes;.\track-20-filesystem\task-12-2-4-master-failover\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
