# Task 1 - Implement Key-Value Interface

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-7-1-kv-interface>

Short title: `KV Interface`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-7-1-kv-interface dependency:copy-dependencies package
Get-Content .\track-07-store\task-7-1-kv-interface\samples\input.jsonl | java -cp '.\track-07-store\task-7-1-kv-interface\target\classes;.\track-07-store\task-7-1-kv-interface\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
