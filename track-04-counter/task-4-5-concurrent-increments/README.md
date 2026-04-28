# Task 5 - Handle Concurrent Increments Across Multiple Nodes

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-4-5-concurrent-increments>

Short title: `Concurrent Updates`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-4-5-concurrent-increments dependency:copy-dependencies package
Get-Content .\track-04-counter\task-4-5-concurrent-increments\samples\input.jsonl | java -cp '.\track-04-counter\task-4-5-concurrent-increments\target\classes;.\track-04-counter\task-4-5-concurrent-increments\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
