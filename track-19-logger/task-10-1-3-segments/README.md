# Task 3 - Add WAL Segment Files with Offset Index

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-3-segments>

Short title: `WAL Segments`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-1-3-segments dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-1-3-segments\samples\input.jsonl | java -cp '.\track-19-logger\task-10-1-3-segments\target\classes;.\track-19-logger\task-10-1-3-segments\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
