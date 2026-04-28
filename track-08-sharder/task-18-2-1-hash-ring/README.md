# Task 6 - Implement a Consistent Hash Ring

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-1-hash-ring>

Short title: `Hash Ring`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-18-2-1-hash-ring dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-18-2-1-hash-ring\samples\input.jsonl | java -cp '.\track-08-sharder\task-18-2-1-hash-ring\target\classes;.\track-08-sharder\task-18-2-1-hash-ring\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
