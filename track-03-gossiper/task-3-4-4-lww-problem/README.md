# Task 19 - Demonstrate LWW Data Loss with Version Vectors

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-4-lww-problem>

Short title: `LWW Problem`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-4-4-lww-problem dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-4-4-lww-problem\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-4-4-lww-problem\target\classes;.\track-03-gossiper\task-3-4-4-lww-problem\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
