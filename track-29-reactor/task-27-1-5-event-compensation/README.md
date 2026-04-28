# Task 5 - Implement Event Compensation and Sagas

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-5-event-compensation>

Short title: `Sagas`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-29-reactor/task-27-1-5-event-compensation dependency:copy-dependencies package
Get-Content .\track-29-reactor\task-27-1-5-event-compensation\samples\input.jsonl | java -cp '.\track-29-reactor\task-27-1-5-event-compensation\target\classes;.\track-29-reactor\task-27-1-5-event-compensation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
