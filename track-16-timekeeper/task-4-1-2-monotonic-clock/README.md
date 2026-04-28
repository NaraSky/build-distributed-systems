# Task 2 - Implement Monotonic Clock Wrapper

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-2-monotonic-clock>

Short title: `Monotonic Clock`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-1-2-monotonic-clock dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-1-2-monotonic-clock\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-1-2-monotonic-clock\target\classes;.\track-16-timekeeper\task-4-1-2-monotonic-clock\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
