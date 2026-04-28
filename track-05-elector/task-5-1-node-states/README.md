# Task 1 - Implement Node States (Leader, Follower, Candidate)

Website: <https://builddistributedsystem.com/tracks/elector/tasks/task-5-1-node-states>

Short title: `Node States`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-05-elector/task-5-1-node-states dependency:copy-dependencies package
Get-Content .\track-05-elector\task-5-1-node-states\samples\input.jsonl | java -cp '.\track-05-elector\task-5-1-node-states\target\classes;.\track-05-elector\task-5-1-node-states\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
