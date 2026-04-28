# Task 4 - Handle RequestVote RPC

Website: <https://builddistributedsystem.com/tracks/elector/tasks/task-5-4-request-vote>

Short title: `RequestVote`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-05-elector/task-5-4-request-vote dependency:copy-dependencies package
Get-Content .\track-05-elector\task-5-4-request-vote\samples\input.jsonl | java -cp '.\track-05-elector\task-5-4-request-vote\target\classes;.\track-05-elector\task-5-4-request-vote\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
