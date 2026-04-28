# Task 3 - Ensure Read Consistency

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-7-3-read-consistency>

Short title: `Read Consistency`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-7-3-read-consistency dependency:copy-dependencies package
Get-Content .\track-07-store\task-7-3-read-consistency\samples\input.jsonl | java -cp '.\track-07-store\task-7-3-read-consistency\target\classes;.\track-07-store\task-7-3-read-consistency\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
