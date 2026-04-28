# Task 5 - Implement CRDTs

Website: <https://builddistributedsystem.com/tracks/advanced/tasks/task-10-5-crdt>

Short title: `CRDTs`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-10-advanced/task-10-5-crdt dependency:copy-dependencies package
Get-Content .\track-10-advanced\task-10-5-crdt\samples\input.jsonl | java -cp '.\track-10-advanced\task-10-5-crdt\target\classes;.\track-10-advanced\task-10-5-crdt\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
