# Task 14 - Analyze CRDT Tradeoffs vs. OCC and Locking

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-4-crdt-tradeoffs>

Short title: `CRDT Tradeoffs`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-17-3-4-crdt-tradeoffs dependency:copy-dependencies package
Get-Content .\track-04-counter\task-17-3-4-crdt-tradeoffs\samples\input.jsonl | java -cp '.\track-04-counter\task-17-3-4-crdt-tradeoffs\target\classes;.\track-04-counter\task-17-3-4-crdt-tradeoffs\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
