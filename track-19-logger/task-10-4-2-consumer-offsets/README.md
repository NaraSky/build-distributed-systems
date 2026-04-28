# Task 17 - Implement Consumer Group Offset Tracking

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-2-consumer-offsets>

Short title: `Consumer Offsets`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-4-2-consumer-offsets dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-4-2-consumer-offsets\samples\input.jsonl | java -cp '.\track-19-logger\task-10-4-2-consumer-offsets\target\classes;.\track-19-logger\task-10-4-2-consumer-offsets\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
