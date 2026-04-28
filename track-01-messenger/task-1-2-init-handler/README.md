# Task 2 - Handle Init Message and Store Cluster Metadata

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-init-handler>

Short title: `Init Handler`

Difficulty: `beginner`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-2-init-handler dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-2-init-handler\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-2-init-handler\target\classes;.\track-01-messenger\task-1-2-init-handler\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
