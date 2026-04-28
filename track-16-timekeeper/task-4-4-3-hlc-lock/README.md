# Task 18 - Implement a Distributed Lock Using HLC Timestamps

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-3-hlc-lock>

Short title: `HLC Lock`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-4-3-hlc-lock dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-4-3-hlc-lock\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-4-3-hlc-lock\target\classes;.\track-16-timekeeper\task-4-4-3-hlc-lock\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
