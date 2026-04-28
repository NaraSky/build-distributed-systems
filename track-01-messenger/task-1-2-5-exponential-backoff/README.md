# Task 10 - Implement Exponential Backoff for Retries

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-5-exponential-backoff>

Short title: `Exponential Backoff`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-2-5-exponential-backoff dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-2-5-exponential-backoff\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-2-5-exponential-backoff\target\classes;.\track-01-messenger\task-1-2-5-exponential-backoff\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
