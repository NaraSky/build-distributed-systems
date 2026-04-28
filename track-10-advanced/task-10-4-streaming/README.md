# Task 4 - Build Stream Processing Pipeline

Website: <https://builddistributedsystem.com/tracks/advanced/tasks/task-10-4-streaming>

Short title: `Streaming`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-10-advanced/task-10-4-streaming dependency:copy-dependencies package
Get-Content .\track-10-advanced\task-10-4-streaming\samples\input.jsonl | java -cp '.\track-10-advanced\task-10-4-streaming\target\classes;.\track-10-advanced\task-10-4-streaming\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
