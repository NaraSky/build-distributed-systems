# Task 2 - Implement Consistent Hashing for Sharding

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-8-2-consistent-hash>

Short title: `Consistent Hash`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-8-2-consistent-hash dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-8-2-consistent-hash\samples\input.jsonl | java -cp '.\track-08-sharder\task-8-2-consistent-hash\target\classes;.\track-08-sharder\task-8-2-consistent-hash\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
