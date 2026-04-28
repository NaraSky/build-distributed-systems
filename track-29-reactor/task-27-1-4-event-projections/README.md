# Task 4 - Implement Event Projections

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-4-event-projections>

Short title: `Event Projections`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-29-reactor/task-27-1-4-event-projections dependency:copy-dependencies package
Get-Content .\track-29-reactor\task-27-1-4-event-projections\samples\input.jsonl | java -cp '.\track-29-reactor\task-27-1-4-event-projections\target\classes;.\track-29-reactor\task-27-1-4-event-projections\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
