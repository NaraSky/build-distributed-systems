# Task 4 - Build Grow-Only Counter (G-Counter) CRDT

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-4-4-g-counter>

Short title: `G-Counter CRDT`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-4-4-g-counter dependency:copy-dependencies package
Get-Content .\track-04-counter\task-4-4-g-counter\samples\input.jsonl | java -cp '.\track-04-counter\task-4-4-g-counter\target\classes;.\track-04-counter\task-4-4-g-counter\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
