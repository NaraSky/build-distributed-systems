# Task 11 - Model Message Format with Typed Schema

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-1-typed-schema>

Short title: `Typed Schema`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-3-1-typed-schema dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-3-1-typed-schema\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-3-1-typed-schema\target\classes;.\track-01-messenger\task-1-3-1-typed-schema\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
