# Task 12 - Implement Optimistic Concurrency Control

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-3-2-occ>

Short title: `OCC`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-8-3-2-occ dependency:copy-dependencies package
Get-Content .\track-07-store\task-8-3-2-occ\samples\input.jsonl | java -cp '.\track-07-store\task-8-3-2-occ\target\classes;.\track-07-store\task-8-3-2-occ\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
