# Task 1 - Implement Database Schema Migrations

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-1-database-migrations>

Short title: `Schema Migrations`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-27-migrator/task-25-1-1-database-migrations dependency:copy-dependencies package
Get-Content .\track-27-migrator\task-25-1-1-database-migrations\samples\input.jsonl | java -cp '.\track-27-migrator\task-25-1-1-database-migrations\target\classes;.\track-27-migrator\task-25-1-1-database-migrations\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
