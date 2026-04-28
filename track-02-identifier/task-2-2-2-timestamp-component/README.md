# Task 7 - Implement Timestamp Component with Custom Epoch

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-2-timestamp-component>

Short title: `Custom Epoch`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-2-2-timestamp-component dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-2-2-timestamp-component\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-2-2-timestamp-component\target\classes;.\track-02-identifier\task-2-2-2-timestamp-component\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
