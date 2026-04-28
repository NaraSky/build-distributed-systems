# Task 1 - Implement Event Store

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-1-event-store>

Short title: `Event Store`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-29-reactor/task-27-1-1-event-store dependency:copy-dependencies package
Get-Content .\track-29-reactor\task-27-1-1-event-store\samples\input.jsonl | java -cp '.\track-29-reactor\task-27-1-1-event-store\target\classes;.\track-29-reactor\task-27-1-1-event-store\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
