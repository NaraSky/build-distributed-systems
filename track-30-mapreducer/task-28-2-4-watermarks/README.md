# Task 9 - Handle Out-of-Order Events with Watermarks

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-4-watermarks>

Short title: `Watermarks`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-30-mapreducer/task-28-2-4-watermarks dependency:copy-dependencies package
Get-Content .\track-30-mapreducer\task-28-2-4-watermarks\samples\input.jsonl | java -cp '.\track-30-mapreducer\task-28-2-4-watermarks\target\classes;.\track-30-mapreducer\task-28-2-4-watermarks\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
