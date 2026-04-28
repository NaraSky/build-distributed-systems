# Task 10 - Build a Service Discovery System

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-5-service-discovery>

Short title: `Service Discovery`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-2-5-service-discovery dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-2-5-service-discovery\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-2-5-service-discovery\target\classes;.\track-22-watcher\task-15-2-5-service-discovery\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
