# Task 5 - Implement Migration Rollback Strategies

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-5-rollback-strategies>

Short title: `Rollback Strategies`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-27-migrator/task-25-1-5-rollback-strategies dependency:copy-dependencies package
Get-Content .\track-27-migrator\task-25-1-5-rollback-strategies\samples\input.jsonl | java -cp '.\track-27-migrator\task-25-1-5-rollback-strategies\target\classes;.\track-27-migrator\task-25-1-5-rollback-strategies\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
