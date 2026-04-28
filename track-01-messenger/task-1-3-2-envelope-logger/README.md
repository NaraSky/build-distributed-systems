# Task 12 - Add Message Envelope Logger with Timestamps

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-2-envelope-logger>

Short title: `Envelope Logger`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-3-2-envelope-logger dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-3-2-envelope-logger\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-3-2-envelope-logger\target\classes;.\track-01-messenger\task-1-3-2-envelope-logger\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
