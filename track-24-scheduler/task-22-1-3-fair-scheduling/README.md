# Task 3 - Implement Fair Job Scheduling

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-3-fair-scheduling>

Short title: `Fair Scheduling`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-24-scheduler/task-22-1-3-fair-scheduling dependency:copy-dependencies package
Get-Content .\track-24-scheduler\task-22-1-3-fair-scheduling\samples\input.jsonl | java -cp '.\track-24-scheduler\task-22-1-3-fair-scheduling\target\classes;.\track-24-scheduler\task-22-1-3-fair-scheduling\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
