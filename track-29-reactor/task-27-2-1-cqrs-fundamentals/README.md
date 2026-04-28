# Task 6 - Implement CQRS Fundamentals

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-1-cqrs-fundamentals>

Short title: `CQRS Fundamentals`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-29-reactor/task-27-2-1-cqrs-fundamentals dependency:copy-dependencies package
Get-Content .\track-29-reactor\task-27-2-1-cqrs-fundamentals\samples\input.jsonl | java -cp '.\track-29-reactor\task-27-2-1-cqrs-fundamentals\target\classes;.\track-29-reactor\task-27-2-1-cqrs-fundamentals\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
