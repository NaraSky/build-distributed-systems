# Task 1 - Implement Basic JSON Message Parser

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-1-json-parser>

Short title: `JSON Parser`

Difficulty: `beginner`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-1-json-parser dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-1-json-parser\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-1-json-parser\target\classes;.\track-01-messenger\task-1-1-json-parser\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
