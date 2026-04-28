# Task 4 - Implement Fault Tolerance in MapReduce

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-4-fault-tolerance>

Short title: `Fault Tolerance`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-30-mapreducer/task-28-1-4-fault-tolerance dependency:copy-dependencies package
Get-Content .\track-30-mapreducer\task-28-1-4-fault-tolerance\samples\input.jsonl | java -cp '.\track-30-mapreducer\task-28-1-4-fault-tolerance\target\classes;.\track-30-mapreducer\task-28-1-4-fault-tolerance\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
