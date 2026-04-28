# Task 1 - Design a GFS-Style Distributed File System Architecture

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-1-architecture>

Short title: `DFS Architecture`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-20-filesystem/task-12-1-1-architecture dependency:copy-dependencies package
Get-Content .\track-20-filesystem\task-12-1-1-architecture\samples\input.jsonl | java -cp '.\track-20-filesystem\task-12-1-1-architecture\target\classes;.\track-20-filesystem\task-12-1-1-architecture\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
