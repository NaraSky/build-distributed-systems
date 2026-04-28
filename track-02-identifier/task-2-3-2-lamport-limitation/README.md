# Task 12 - Demonstrate Lamport Clock Causality Limitation

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-2-lamport-limitation>

Short title: `Causality Limitation`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-3-2-lamport-limitation dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-3-2-lamport-limitation\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-3-2-lamport-limitation\target\classes;.\track-02-identifier\task-2-3-2-lamport-limitation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
