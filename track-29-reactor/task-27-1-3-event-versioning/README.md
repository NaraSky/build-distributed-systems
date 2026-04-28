# Task 3 - Implement Event Versioning and Migration

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-3-event-versioning>

Short title: `Event Versioning`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-29-reactor/task-27-1-3-event-versioning dependency:copy-dependencies package
Get-Content .\track-29-reactor\task-27-1-3-event-versioning\samples\input.jsonl | java -cp '.\track-29-reactor\task-27-1-3-event-versioning\target\classes;.\track-29-reactor\task-27-1-3-event-versioning\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
