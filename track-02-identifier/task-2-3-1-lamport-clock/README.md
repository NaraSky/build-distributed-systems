# Task 11 - Implement a Lamport Clock

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-1-lamport-clock>

Short title: `Lamport Clock`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-3-1-lamport-clock dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-3-1-lamport-clock\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-3-1-lamport-clock\target\classes;.\track-02-identifier\task-2-3-1-lamport-clock\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
