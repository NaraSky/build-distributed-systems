# Task 8 - Implement Sequence Counter with Overflow Handling

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-3-sequence-counter>

Short title: `Sequence Counter`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-2-3-sequence-counter dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-2-3-sequence-counter\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-2-3-sequence-counter\target\classes;.\track-02-identifier\task-2-2-3-sequence-counter\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
