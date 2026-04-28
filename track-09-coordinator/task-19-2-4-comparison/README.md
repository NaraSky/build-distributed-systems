# Task 9 - Compare 2PC vs 3PC Protocols

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-4-comparison>

Short title: `2PC vs 3PC Comparison`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-19-2-4-comparison dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-19-2-4-comparison\samples\input.jsonl | java -cp '.\track-09-coordinator\task-19-2-4-comparison\target\classes;.\track-09-coordinator\task-19-2-4-comparison\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
