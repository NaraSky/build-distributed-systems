# Task 15 - Implement Distributed ORDER BY with LIMIT

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-5-order-limit>

Short title: `Distributed ORDER BY LIMIT`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-18-3-5-order-limit dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-18-3-5-order-limit\samples\input.jsonl | java -cp '.\track-08-sharder\task-18-3-5-order-limit\target\classes;.\track-08-sharder\task-18-3-5-order-limit\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
