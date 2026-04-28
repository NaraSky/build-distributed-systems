# Task 5 - Wait-Out-Uncertainty for External Consistency

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-5-wait-out-uncertainty>

Short title: `Wait Uncertainty`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-1-5-wait-out-uncertainty dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-1-5-wait-out-uncertainty\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-1-5-wait-out-uncertainty\target\classes;.\track-16-timekeeper\task-4-1-5-wait-out-uncertainty\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
