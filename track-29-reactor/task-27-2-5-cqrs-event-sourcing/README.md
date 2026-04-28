# Task 10 - Implement CQRS with Event Sourcing

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-5-cqrs-event-sourcing>

Short title: `CQRS + Event Sourcing`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-29-reactor/task-27-2-5-cqrs-event-sourcing dependency:copy-dependencies package
Get-Content .\track-29-reactor\task-27-2-5-cqrs-event-sourcing\samples\input.jsonl | java -cp '.\track-29-reactor\task-27-2-5-cqrs-event-sourcing\target\classes;.\track-29-reactor\task-27-2-5-cqrs-event-sourcing\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
