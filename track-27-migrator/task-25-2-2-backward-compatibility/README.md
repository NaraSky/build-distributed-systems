# Task 7 - Implement Backward-Compatible API Changes

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-2-backward-compatibility>

Short title: `Backward Compatibility`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-27-migrator/task-25-2-2-backward-compatibility dependency:copy-dependencies package
Get-Content .\track-27-migrator\task-25-2-2-backward-compatibility\samples\input.jsonl | java -cp '.\track-27-migrator\task-25-2-2-backward-compatibility\target\classes;.\track-27-migrator\task-25-2-2-backward-compatibility\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
