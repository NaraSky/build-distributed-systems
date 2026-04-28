# Task 3 - Implement Secure Session Management

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-3-session-management>

Short title: `Session Management`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-26-securitor/task-24-1-3-session-management dependency:copy-dependencies package
Get-Content .\track-26-securitor\task-24-1-3-session-management\samples\input.jsonl | java -cp '.\track-26-securitor\task-24-1-3-session-management\target\classes;.\track-26-securitor\task-24-1-3-session-management\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
