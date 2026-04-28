# Task 10 - Pass the Maelstrom G-Counter Workload

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-5-maelstrom-counter>

Short title: `Maelstrom Counter`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-17-2-5-maelstrom-counter dependency:copy-dependencies package
Get-Content .\track-04-counter\task-17-2-5-maelstrom-counter\samples\input.jsonl | java -cp '.\track-04-counter\task-17-2-5-maelstrom-counter\target\classes;.\track-04-counter\task-17-2-5-maelstrom-counter\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
