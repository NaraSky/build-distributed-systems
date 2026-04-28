# Task 2 - Implement Backward-Compatible Schema Migrations

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-2-backward-compatible-migrations>

Short title: `Backward-Compatible Migrations`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-27-migrator/task-25-1-2-backward-compatible-migrations dependency:copy-dependencies package
Get-Content .\track-27-migrator\task-25-1-2-backward-compatible-migrations\samples\input.jsonl | java -cp '.\track-27-migrator\task-25-1-2-backward-compatible-migrations\target\classes;.\track-27-migrator\task-25-1-2-backward-compatible-migrations\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
