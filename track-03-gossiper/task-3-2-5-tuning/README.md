# Task 10 - Tune Gossip Parameters for Maelstrom Broadcast

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-5-tuning>

Short title: `Gossip Tuning`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-2-5-tuning dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-2-5-tuning\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-2-5-tuning\target\classes;.\track-03-gossiper\task-3-2-5-tuning\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
