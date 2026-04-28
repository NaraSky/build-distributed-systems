# Task 4 - Implement Data Migrations

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-4-data-migrations>

Short title: `Data Migrations`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-27-migrator/task-25-1-4-data-migrations dependency:copy-dependencies package
Get-Content .\track-27-migrator\task-25-1-4-data-migrations\samples\input.jsonl | java -cp '.\track-27-migrator\task-25-1-4-data-migrations\target\classes;.\track-27-migrator\task-25-1-4-data-migrations\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
