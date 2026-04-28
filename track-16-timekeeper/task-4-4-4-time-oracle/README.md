# Task 19 - Build a Time Oracle Service with Failover

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-4-time-oracle>

Short title: `Time Oracle`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-4-4-time-oracle dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-4-4-time-oracle\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-4-4-time-oracle\target\classes;.\track-16-timekeeper\task-4-4-4-time-oracle\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
