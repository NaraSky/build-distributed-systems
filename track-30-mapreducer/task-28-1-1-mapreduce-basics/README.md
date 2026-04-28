# Task 1 - Implement Single-Machine MapReduce

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-1-mapreduce-basics>

Short title: `MapReduce Basics`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-30-mapreducer/task-28-1-1-mapreduce-basics dependency:copy-dependencies package
Get-Content .\track-30-mapreducer\task-28-1-1-mapreduce-basics\samples\input.jsonl | java -cp '.\track-30-mapreducer\task-28-1-1-mapreduce-basics\target\classes;.\track-30-mapreducer\task-28-1-1-mapreduce-basics\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
