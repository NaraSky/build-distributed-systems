# Task 19 - Implement In-Sync Replicas (ISR) Management

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-4-isr>

Short title: `ISR Management`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-4-4-isr dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-4-4-isr\samples\input.jsonl | java -cp '.\track-19-logger\task-10-4-4-isr\target\classes;.\track-19-logger\task-10-4-4-isr\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
