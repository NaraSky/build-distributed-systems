# Task 8 - Implement a PN-Counter for Increment and Decrement

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-3-pn-counter>

Short title: `PN-Counter`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-17-2-3-pn-counter dependency:copy-dependencies package
Get-Content .\track-04-counter\task-17-2-3-pn-counter\samples\input.jsonl | java -cp '.\track-04-counter\task-17-2-3-pn-counter\target\classes;.\track-04-counter\task-17-2-3-pn-counter\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
