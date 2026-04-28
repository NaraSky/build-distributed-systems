# Task 1 - Implement MapReduce

Website: <https://builddistributedsystem.com/tracks/advanced/tasks/task-10-1-mapreduce>

Short title: `MapReduce`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-10-advanced/task-10-1-mapreduce dependency:copy-dependencies package
Get-Content .\track-10-advanced\task-10-1-mapreduce\samples\input.jsonl | java -cp '.\track-10-advanced\task-10-1-mapreduce\target\classes;.\track-10-advanced\task-10-1-mapreduce\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
