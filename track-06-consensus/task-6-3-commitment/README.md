# Task 3 - Implement Entry Commitment

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-6-3-commitment>

Short title: `Commitment`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-6-3-commitment dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-6-3-commitment\samples\input.jsonl | java -cp '.\track-06-consensus\task-6-3-commitment\target\classes;.\track-06-consensus\task-6-3-commitment\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
