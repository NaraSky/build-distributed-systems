# Task 16 - Understand and Implement HLC Format

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-1-hlc-format>

Short title: `HLC Format`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-4-1-hlc-format dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-4-1-hlc-format\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-4-1-hlc-format\target\classes;.\track-02-identifier\task-2-4-1-hlc-format\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
