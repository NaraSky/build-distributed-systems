# Task 17 - Implement Simplified PBFT with 4 Nodes

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-2-pbft-impl>

Short title: `PBFT Implementation`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-4-2-pbft-impl dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-4-2-pbft-impl\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-4-2-pbft-impl\target\classes;.\track-06-consensus\task-7-4-2-pbft-impl\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
