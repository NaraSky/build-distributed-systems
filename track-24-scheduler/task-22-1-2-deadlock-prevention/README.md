# Task 2 - Implement Deadlock Prevention in Scheduling

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-2-deadlock-prevention>

Short title: `Deadlock Prevention`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-24-scheduler/task-22-1-2-deadlock-prevention dependency:copy-dependencies package
Get-Content .\track-24-scheduler\task-22-1-2-deadlock-prevention\samples\input.jsonl | java -cp '.\track-24-scheduler\task-22-1-2-deadlock-prevention\target\classes;.\track-24-scheduler\task-22-1-2-deadlock-prevention\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
