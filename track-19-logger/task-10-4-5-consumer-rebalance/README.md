# Task 20 - Implement Consumer Group Rebalancing

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-5-consumer-rebalance>

Short title: `Consumer Rebalance`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-4-5-consumer-rebalance dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-4-5-consumer-rebalance\samples\input.jsonl | java -cp '.\track-19-logger\task-10-4-5-consumer-rebalance\target\classes;.\track-19-logger\task-10-4-5-consumer-rebalance\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
