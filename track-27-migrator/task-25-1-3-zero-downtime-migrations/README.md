# Task 3 - Implement Zero-Downtime Database Migrations

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-3-zero-downtime-migrations>

Short title: `Zero-Downtime Migrations`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-27-migrator/task-25-1-3-zero-downtime-migrations dependency:copy-dependencies package
Get-Content .\track-27-migrator\task-25-1-3-zero-downtime-migrations\samples\input.jsonl | java -cp '.\track-27-migrator\task-25-1-3-zero-downtime-migrations\target\classes;.\track-27-migrator\task-25-1-3-zero-downtime-migrations\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
