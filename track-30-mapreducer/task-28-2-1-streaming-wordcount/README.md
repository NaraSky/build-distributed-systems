# Task 6 - Implement Streaming Word Count

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-1-streaming-wordcount>

Short title: `Streaming Word Count`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-30-mapreducer/task-28-2-1-streaming-wordcount dependency:copy-dependencies package
Get-Content .\track-30-mapreducer\task-28-2-1-streaming-wordcount\samples\input.jsonl | java -cp '.\track-30-mapreducer\task-28-2-1-streaming-wordcount\target\classes;.\track-30-mapreducer\task-28-2-1-streaming-wordcount\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
