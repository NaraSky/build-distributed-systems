# Task 2 - Implement the Master Namespace Tree

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-2-namespace>

Short title: `Master Namespace`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-20-filesystem/task-12-1-2-namespace dependency:copy-dependencies package
Get-Content .\track-20-filesystem\task-12-1-2-namespace\samples\input.jsonl | java -cp '.\track-20-filesystem\task-12-1-2-namespace\target\classes;.\track-20-filesystem\task-12-1-2-namespace\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
