# Task 1 - Generate Unique IDs Using Node ID and Timestamp

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-1-basic-id>

Short title: `Basic ID Generation`

Difficulty: `beginner`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-1-basic-id dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-1-basic-id\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-1-basic-id\target\classes;.\track-02-identifier\task-2-1-basic-id\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
