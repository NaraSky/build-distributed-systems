# Task 1 - Implement Basic Counter with Lost Update Problem

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-4-1-lost-update>

Short title: `Lost Updates`

Difficulty: `beginner`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-4-1-lost-update dependency:copy-dependencies package
Get-Content .\track-04-counter\task-4-1-lost-update\samples\input.jsonl | java -cp '.\track-04-counter\task-4-1-lost-update\target\classes;.\track-04-counter\task-4-1-lost-update\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
