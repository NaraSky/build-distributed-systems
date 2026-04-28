# Task 16 - Implement Hybrid Logical Clocks

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-1-hlc-impl>

Short title: `HLC Implementation`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-4-1-hlc-impl dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-4-1-hlc-impl\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-4-1-hlc-impl\target\classes;.\track-16-timekeeper\task-4-4-1-hlc-impl\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
