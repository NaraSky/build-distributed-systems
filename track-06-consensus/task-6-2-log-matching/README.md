# Task 2 - Ensure Log Matching Property

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-6-2-log-matching>

Short title: `Log Matching`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-6-2-log-matching dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-6-2-log-matching\samples\input.jsonl | java -cp '.\track-06-consensus\task-6-2-log-matching\target\classes;.\track-06-consensus\task-6-2-log-matching\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
