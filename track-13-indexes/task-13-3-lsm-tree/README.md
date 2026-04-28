# Task 3 - Implement LSM Tree

Website: <https://builddistributedsystem.com/tracks/indexes/tasks/task-13-3-lsm-tree>

Short title: `LSM Tree`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-13-indexes/task-13-3-lsm-tree dependency:copy-dependencies package
Get-Content .\track-13-indexes\task-13-3-lsm-tree\samples\input.jsonl | java -cp '.\track-13-indexes\task-13-3-lsm-tree\target\classes;.\track-13-indexes\task-13-3-lsm-tree\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
