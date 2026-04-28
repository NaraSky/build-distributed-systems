# Task 8 - Implement Sliding Windows

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-3-sliding-windows>

Short title: `Sliding Windows`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-30-mapreducer/task-28-2-3-sliding-windows dependency:copy-dependencies package
Get-Content .\track-30-mapreducer\task-28-2-3-sliding-windows\samples\input.jsonl | java -cp '.\track-30-mapreducer\task-28-2-3-sliding-windows\target\classes;.\track-30-mapreducer\task-28-2-3-sliding-windows\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
