# Task 9 - Implement Protocol Evolution

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-4-protocol-evolution>

Short title: `Protocol Evolution`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-27-migrator/task-25-2-4-protocol-evolution dependency:copy-dependencies package
Get-Content .\track-27-migrator\task-25-2-4-protocol-evolution\samples\input.jsonl | java -cp '.\track-27-migrator\task-25-2-4-protocol-evolution\target\classes;.\track-27-migrator\task-25-2-4-protocol-evolution\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
