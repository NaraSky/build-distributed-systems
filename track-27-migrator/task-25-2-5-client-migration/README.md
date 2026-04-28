# Task 10 - Implement Client Migration Strategy

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-5-client-migration>

Short title: `Client Migration`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-27-migrator/task-25-2-5-client-migration dependency:copy-dependencies package
Get-Content .\track-27-migrator\task-25-2-5-client-migration\samples\input.jsonl | java -cp '.\track-27-migrator\task-25-2-5-client-migration\target\classes;.\track-27-migrator\task-25-2-5-client-migration\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
