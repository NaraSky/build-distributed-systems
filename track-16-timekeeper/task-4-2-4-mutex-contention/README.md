# Task 9 - Simulate Concurrent Mutex Requests from Multiple Nodes

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-4-mutex-contention>

Short title: `Mutex Contention`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-2-4-mutex-contention dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-2-4-mutex-contention\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-2-4-mutex-contention\target\classes;.\track-16-timekeeper\task-4-2-4-mutex-contention\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
