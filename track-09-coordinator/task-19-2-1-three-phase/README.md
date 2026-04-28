# Task 6 - Implement Three-Phase Commit Protocol

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-1-three-phase>

Short title: `Three-Phase Commit`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-19-2-1-three-phase dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-19-2-1-three-phase\samples\input.jsonl | java -cp '.\track-09-coordinator\task-19-2-1-three-phase\target\classes;.\track-09-coordinator\task-19-2-1-three-phase\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
