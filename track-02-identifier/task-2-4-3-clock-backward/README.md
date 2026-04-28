# Task 18 - HLC Handles Backward Clock Gracefully

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-3-clock-backward>

Short title: `Clock Backward`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-4-3-clock-backward dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-4-3-clock-backward\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-4-3-clock-backward\target\classes;.\track-02-identifier\task-2-4-3-clock-backward\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
