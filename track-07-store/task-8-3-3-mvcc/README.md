# Task 13 - Implement Multi-Version Concurrency Control

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-3-3-mvcc>

Short title: `MVCC`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-8-3-3-mvcc dependency:copy-dependencies package
Get-Content .\track-07-store\task-8-3-3-mvcc\samples\input.jsonl | java -cp '.\track-07-store\task-8-3-3-mvcc\target\classes;.\track-07-store\task-8-3-3-mvcc\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
