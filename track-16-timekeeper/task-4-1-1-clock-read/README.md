# Task 1 - Read System Clock and Detect Backward Jumps

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-1-clock-read>

Short title: `Clock Read`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-1-1-clock-read dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-1-1-clock-read\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-1-1-clock-read\target\classes;.\track-16-timekeeper\task-4-1-1-clock-read\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
