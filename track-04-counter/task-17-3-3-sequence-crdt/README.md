# Task 13 - Implement a Sequence CRDT for Collaborative Text Editing

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-3-sequence-crdt>

Short title: `Sequence CRDT`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-17-3-3-sequence-crdt dependency:copy-dependencies package
Get-Content .\track-04-counter\task-17-3-3-sequence-crdt\samples\input.jsonl | java -cp '.\track-04-counter\task-17-3-3-sequence-crdt\target\classes;.\track-04-counter\task-17-3-3-sequence-crdt\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
