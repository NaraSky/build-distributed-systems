# Task 3 - Simulate Split-Brain Caused by Clock Drift

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-3-split-brain-lease>

Short title: `Split-Brain Lease`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-1-3-split-brain-lease dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-1-3-split-brain-lease\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-1-3-split-brain-lease\target\classes;.\track-16-timekeeper\task-4-1-3-split-brain-lease\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
