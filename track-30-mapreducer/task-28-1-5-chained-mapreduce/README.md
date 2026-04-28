# Task 5 - Implement Chained MapReduce Pipeline

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-5-chained-mapreduce>

Short title: `Chained MapReduce`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-30-mapreducer/task-28-1-5-chained-mapreduce dependency:copy-dependencies package
Get-Content .\track-30-mapreducer\task-28-1-5-chained-mapreduce\samples\input.jsonl | java -cp '.\track-30-mapreducer\task-28-1-5-chained-mapreduce\target\classes;.\track-30-mapreducer\task-28-1-5-chained-mapreduce\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
