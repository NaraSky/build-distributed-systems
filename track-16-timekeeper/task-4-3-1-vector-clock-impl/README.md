# Task 11 - Implement Vector Clocks

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-1-vector-clock-impl>

Short title: `Vector Clock Impl`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-3-1-vector-clock-impl dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-3-1-vector-clock-impl\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-3-1-vector-clock-impl\target\classes;.\track-16-timekeeper\task-4-3-1-vector-clock-impl\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
