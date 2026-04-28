# Task 7 - Implement the Apply Channel for State Machine

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-2-apply-channel>

Short title: `Apply Channel`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-2-2-apply-channel dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-2-2-apply-channel\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-2-2-apply-channel\target\classes;.\track-06-consensus\task-7-2-2-apply-channel\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
