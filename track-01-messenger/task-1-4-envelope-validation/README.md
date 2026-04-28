# Task 4 - Add Message Envelope Validation

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-4-envelope-validation>

Short title: `Envelope Validation`

Difficulty: `beginner`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-4-envelope-validation dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-4-envelope-validation\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-4-envelope-validation\target\classes;.\track-01-messenger\task-1-4-envelope-validation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
