# Task 2 - Add a Connection Pool with Configurable Backlog

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-2-connection-pool>

Short title: `Connection Pool`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-1-2-connection-pool dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-1-2-connection-pool\samples\input.jsonl | java -cp '.\track-17-networker\task-5-1-2-connection-pool\target\classes;.\track-17-networker\task-5-1-2-connection-pool\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
