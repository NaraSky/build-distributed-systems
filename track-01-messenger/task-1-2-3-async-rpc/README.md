# Task 8 - Implement Async RPC Using Callbacks

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-3-async-rpc>

Short title: `Async RPC`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-2-3-async-rpc dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-2-3-async-rpc\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-2-3-async-rpc\target\classes;.\track-01-messenger\task-1-2-3-async-rpc\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
