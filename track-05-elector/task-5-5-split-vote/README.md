# Task 5 - Prevent Split Votes Through Term Management

Website: <https://builddistributedsystem.com/tracks/elector/tasks/task-5-5-split-vote>

Short title: `Term Management`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-05-elector/task-5-5-split-vote dependency:copy-dependencies package
Get-Content .\track-05-elector\task-5-5-split-vote\samples\input.jsonl | java -cp '.\track-05-elector\task-5-5-split-vote\target\classes;.\track-05-elector\task-5-5-split-vote\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
