# Task 2 - Add Heartbeat Mechanism

Website: <https://builddistributedsystem.com/tracks/elector/tasks/task-5-2-heartbeat>

Short title: `Heartbeat`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-05-elector/task-5-2-heartbeat dependency:copy-dependencies package
Get-Content .\track-05-elector\task-5-2-heartbeat\samples\input.jsonl | java -cp '.\track-05-elector\task-5-2-heartbeat\target\classes;.\track-05-elector\task-5-2-heartbeat\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
