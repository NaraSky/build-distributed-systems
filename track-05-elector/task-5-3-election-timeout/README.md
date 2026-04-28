# Task 3 - Implement Randomized Election Timeout

Website: <https://builddistributedsystem.com/tracks/elector/tasks/task-5-3-election-timeout>

Short title: `Election Timeout`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-05-elector/task-5-3-election-timeout dependency:copy-dependencies package
Get-Content .\track-05-elector\task-5-3-election-timeout\samples\input.jsonl | java -cp '.\track-05-elector\task-5-3-election-timeout\target\classes;.\track-05-elector\task-5-3-election-timeout\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
