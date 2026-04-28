# Task 6 - Implement the Raft Commitment Rule

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-1-commit-rule>

Short title: `Commit Rule`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-2-1-commit-rule dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-2-1-commit-rule\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-2-1-commit-rule\target\classes;.\track-06-consensus\task-7-2-1-commit-rule\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
