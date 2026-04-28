# Task 10 - Handle Node Failure with Replica Promotion

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-5-node-failure>

Short title: `Node Failure`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-23-searcher/task-16-2-5-node-failure dependency:copy-dependencies package
Get-Content .\track-23-searcher\task-16-2-5-node-failure\samples\input.jsonl | java -cp '.\track-23-searcher\task-16-2-5-node-failure\target\classes;.\track-23-searcher\task-16-2-5-node-failure\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
