# Task 6 - Implement Synchronous RPC with Timeout

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-1-sync-rpc>

Short title: `Sync RPC`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-2-1-sync-rpc dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-2-1-sync-rpc\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-2-1-sync-rpc\target\classes;.\track-01-messenger\task-1-2-1-sync-rpc\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
