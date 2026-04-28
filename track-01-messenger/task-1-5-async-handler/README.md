# Task 5 - Create Async Event Loop for Concurrent Message Handling

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-5-async-handler>

Short title: `Async Handler`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-5-async-handler dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-5-async-handler\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-5-async-handler\target\classes;.\track-01-messenger\task-1-5-async-handler\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
