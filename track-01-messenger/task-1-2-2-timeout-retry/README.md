# Task 7 - Implement Timeout and Retry Loop for RPC

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-2-timeout-retry>

Short title: `Timeout & Retry`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-2-2-timeout-retry dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-2-2-timeout-retry\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-2-2-timeout-retry\target\classes;.\track-01-messenger\task-1-2-2-timeout-retry\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
