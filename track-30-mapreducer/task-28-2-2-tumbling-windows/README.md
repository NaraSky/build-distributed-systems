# Task 7 - Implement Tumbling Windows

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-2-tumbling-windows>

Short title: `Tumbling Windows`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-30-mapreducer/task-28-2-2-tumbling-windows dependency:copy-dependencies package
Get-Content .\track-30-mapreducer\task-28-2-2-tumbling-windows\samples\input.jsonl | java -cp '.\track-30-mapreducer\task-28-2-2-tumbling-windows\target\classes;.\track-30-mapreducer\task-28-2-2-tumbling-windows\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
