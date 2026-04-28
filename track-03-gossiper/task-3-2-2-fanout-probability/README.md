# Task 7 - Calculate Minimum Fanout for Reliable Delivery

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-2-fanout-probability>

Short title: `Fanout Probability`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-2-2-fanout-probability dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-2-2-fanout-probability\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-2-2-fanout-probability\target\classes;.\track-03-gossiper\task-3-2-2-fanout-probability\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
