# Task 2 - Implement Distributed MapReduce

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-2-distributed-mapreduce>

Short title: `Distributed MapReduce`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-30-mapreducer/task-28-1-2-distributed-mapreduce dependency:copy-dependencies package
Get-Content .\track-30-mapreducer\task-28-1-2-distributed-mapreduce\samples\input.jsonl | java -cp '.\track-30-mapreducer\task-28-1-2-distributed-mapreduce\target\classes;.\track-30-mapreducer\task-28-1-2-distributed-mapreduce\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
