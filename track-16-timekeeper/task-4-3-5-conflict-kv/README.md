# Task 15 - Build a Conflict-Detecting Key-Value Store

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-5-conflict-kv>

Short title: `Conflict KV`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-3-5-conflict-kv dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-3-5-conflict-kv\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-3-5-conflict-kv\target\classes;.\track-16-timekeeper\task-4-3-5-conflict-kv\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
