# Task 3 - Implement Graceful Shutdown with In-Flight Drain

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-3-graceful-shutdown>

Short title: `Graceful Shutdown`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-1-3-graceful-shutdown dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-1-3-graceful-shutdown\samples\input.jsonl | java -cp '.\track-17-networker\task-5-1-3-graceful-shutdown\target\classes;.\track-17-networker\task-5-1-3-graceful-shutdown\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
