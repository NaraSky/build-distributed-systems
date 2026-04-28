# Task 19 - Compare HLC, UUID v4, and Snowflake IDs

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-4-id-comparison>

Short title: `ID Comparison`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-4-4-id-comparison dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-4-4-id-comparison\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-4-4-id-comparison\target\classes;.\track-02-identifier\task-2-4-4-id-comparison\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
