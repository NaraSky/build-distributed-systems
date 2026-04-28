# Task 9 - Implement Event-Driven Read Model Updates

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-4-event-driven-updates>

Short title: `Event-Driven Updates`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-29-reactor/task-27-2-4-event-driven-updates dependency:copy-dependencies package
Get-Content .\track-29-reactor\task-27-2-4-event-driven-updates\samples\input.jsonl | java -cp '.\track-29-reactor\task-27-2-4-event-driven-updates\target\classes;.\track-29-reactor\task-27-2-4-event-driven-updates\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
