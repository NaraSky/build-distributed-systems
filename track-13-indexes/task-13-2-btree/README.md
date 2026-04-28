# Task 2 - Build B-Tree Index

Website: <https://builddistributedsystem.com/tracks/indexes/tasks/task-13-2-btree>

Short title: `B-Tree Index`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-13-indexes/task-13-2-btree dependency:copy-dependencies package
Get-Content .\track-13-indexes\task-13-2-btree\samples\input.jsonl | java -cp '.\track-13-indexes\task-13-2-btree\target\classes;.\track-13-indexes\task-13-2-btree\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
