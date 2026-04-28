# Task 9 - Implement Callback Reaper for Leaked RPCs

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-4-callback-reaper>

Short title: `Callback Reaper`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-2-4-callback-reaper dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-2-4-callback-reaper\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-2-4-callback-reaper\target\classes;.\track-01-messenger\task-1-2-4-callback-reaper\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
