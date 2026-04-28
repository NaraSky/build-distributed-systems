# Task 11 - Implement an OR-Set (Observed-Remove Set)

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-1-or-set>

Short title: `OR-Set`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-17-3-1-or-set dependency:copy-dependencies package
Get-Content .\track-04-counter\task-17-3-1-or-set\samples\input.jsonl | java -cp '.\track-04-counter\task-17-3-1-or-set\target\classes;.\track-04-counter\task-17-3-1-or-set\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
