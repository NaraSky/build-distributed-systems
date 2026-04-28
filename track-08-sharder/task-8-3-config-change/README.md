# Task 3 - Handle Configuration Changes

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-8-3-config-change>

Short title: `Config Change`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-8-3-config-change dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-8-3-config-change\samples\input.jsonl | java -cp '.\track-08-sharder\task-8-3-config-change\target\classes;.\track-08-sharder\task-8-3-config-change\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
