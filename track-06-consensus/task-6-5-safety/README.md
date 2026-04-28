# Task 5 - Implement Election Restriction for Safety

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-6-5-safety>

Short title: `Safety`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-6-5-safety dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-6-5-safety\samples\input.jsonl | java -cp '.\track-06-consensus\task-6-5-safety\target\classes;.\track-06-consensus\task-6-5-safety\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
