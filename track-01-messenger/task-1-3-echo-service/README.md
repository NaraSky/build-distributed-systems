# Task 3 - Implement Echo Service with Proper Acknowledgment

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-echo-service>

Short title: `Echo Service`

Difficulty: `beginner`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-3-echo-service dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-3-echo-service\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-3-echo-service\target\classes;.\track-01-messenger\task-1-3-echo-service\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
