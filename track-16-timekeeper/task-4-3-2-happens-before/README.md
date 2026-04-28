# Task 12 - Implement Happens-Before and Concurrency Detection

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-2-happens-before>

Short title: `Happens-Before`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-3-2-happens-before dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-3-2-happens-before\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-3-2-happens-before\target\classes;.\track-16-timekeeper\task-4-3-2-happens-before\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
