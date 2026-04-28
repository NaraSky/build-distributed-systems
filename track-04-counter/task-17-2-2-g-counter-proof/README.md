# Task 7 - Prove G-Counter CRDT Properties

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-2-g-counter-proof>

Short title: `CRDT Proof`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-17-2-2-g-counter-proof dependency:copy-dependencies package
Get-Content .\track-04-counter\task-17-2-2-g-counter-proof\samples\input.jsonl | java -cp '.\track-04-counter\task-17-2-2-g-counter-proof\target\classes;.\track-04-counter\task-17-2-2-g-counter-proof\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
