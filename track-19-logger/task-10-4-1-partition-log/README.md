# Task 16 - Model a Kafka Partition as a Write-Ahead Log

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-1-partition-log>

Short title: `Partition Log`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-4-1-partition-log dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-4-1-partition-log\samples\input.jsonl | java -cp '.\track-19-logger\task-10-4-1-partition-log\target\classes;.\track-19-logger\task-10-4-1-partition-log\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
