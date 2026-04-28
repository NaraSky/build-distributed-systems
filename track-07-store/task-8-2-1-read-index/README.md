# Task 6 - Implement Read Index for Linearizable Reads

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-2-1-read-index>

Short title: `Read Index`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-8-2-1-read-index dependency:copy-dependencies package
Get-Content .\track-07-store\task-8-2-1-read-index\samples\input.jsonl | java -cp '.\track-07-store\task-8-2-1-read-index\target\classes;.\track-07-store\task-8-2-1-read-index\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
