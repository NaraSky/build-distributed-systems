# Task 3 - Implement Shuffle Phase with Hash Partitioning

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-3-shuffle-phase>

Short title: `Shuffle Phase`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-30-mapreducer/task-28-1-3-shuffle-phase dependency:copy-dependencies package
Get-Content .\track-30-mapreducer\task-28-1-3-shuffle-phase\samples\input.jsonl | java -cp '.\track-30-mapreducer\task-28-1-3-shuffle-phase\target\classes;.\track-30-mapreducer\task-28-1-3-shuffle-phase\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
