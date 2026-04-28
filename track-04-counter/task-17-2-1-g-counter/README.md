# Task 6 - Implement a G-Counter (Grow-Only CRDT)

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-1-g-counter>

Short title: `G-Counter`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-17-2-1-g-counter dependency:copy-dependencies package
Get-Content .\track-04-counter\task-17-2-1-g-counter\samples\input.jsonl | java -cp '.\track-04-counter\task-17-2-1-g-counter\target\classes;.\track-04-counter\task-17-2-1-g-counter\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
