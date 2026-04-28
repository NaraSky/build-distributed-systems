# Task 8 - Implement Graceful API Degradation

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-3-graceful-degradation>

Short title: `Graceful Degradation`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-27-migrator/task-25-2-3-graceful-degradation dependency:copy-dependencies package
Get-Content .\track-27-migrator\task-25-2-3-graceful-degradation\samples\input.jsonl | java -cp '.\track-27-migrator\task-25-2-3-graceful-degradation\target\classes;.\track-27-migrator\task-25-2-3-graceful-degradation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
