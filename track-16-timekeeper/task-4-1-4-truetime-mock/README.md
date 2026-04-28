# Task 4 - Implement Mock TrueTime API

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-4-truetime-mock>

Short title: `TrueTime Mock`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-1-4-truetime-mock dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-1-4-truetime-mock\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-1-4-truetime-mock\target\classes;.\track-16-timekeeper\task-4-1-4-truetime-mock\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
