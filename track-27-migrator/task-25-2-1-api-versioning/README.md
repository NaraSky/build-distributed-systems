# Task 6 - Implement API Versioning

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-1-api-versioning>

Short title: `API Versioning`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-27-migrator/task-25-2-1-api-versioning dependency:copy-dependencies package
Get-Content .\track-27-migrator\task-25-2-1-api-versioning\samples\input.jsonl | java -cp '.\track-27-migrator\task-25-2-1-api-versioning\target\classes;.\track-27-migrator\task-25-2-1-api-versioning\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
