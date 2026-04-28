# Task 10 - Compare Mutex Algorithms: Lamport vs Token Ring vs Centralized

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-5-mutex-comparison>

Short title: `Mutex Comparison`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-2-5-mutex-comparison dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-2-5-mutex-comparison\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-2-5-mutex-comparison\target\classes;.\track-16-timekeeper\task-4-2-5-mutex-comparison\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
