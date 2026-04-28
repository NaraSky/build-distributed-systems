# Task 2 - Implement Event Replay

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-2-event-replay>

Short title: `Event Replay`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-29-reactor/task-27-1-2-event-replay dependency:copy-dependencies package
Get-Content .\track-29-reactor\task-27-1-2-event-replay\samples\input.jsonl | java -cp '.\track-29-reactor\task-27-1-2-event-replay\target\classes;.\track-29-reactor\task-27-1-2-event-replay\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
