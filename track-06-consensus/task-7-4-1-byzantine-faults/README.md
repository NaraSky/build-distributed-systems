# Task 16 - Understand Byzantine Faults with Real-World Examples

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-1-byzantine-faults>

Short title: `Byzantine Faults`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-4-1-byzantine-faults dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-4-1-byzantine-faults\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-4-1-byzantine-faults\target\classes;.\track-06-consensus\task-7-4-1-byzantine-faults\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
