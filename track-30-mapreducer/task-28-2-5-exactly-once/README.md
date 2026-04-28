# Task 10 - Implement Exactly-Once Processing

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-5-exactly-once>

Short title: `Exactly-Once`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-30-mapreducer/task-28-2-5-exactly-once dependency:copy-dependencies package
Get-Content .\track-30-mapreducer\task-28-2-5-exactly-once\samples\input.jsonl | java -cp '.\track-30-mapreducer\task-28-2-5-exactly-once\target\classes;.\track-30-mapreducer\task-28-2-5-exactly-once\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
