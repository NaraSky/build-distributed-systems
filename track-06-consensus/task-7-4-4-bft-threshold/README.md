# Task 19 - Prove the N >= 3f+1 Byzantine Fault Threshold

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-4-bft-threshold>

Short title: `BFT Threshold`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-4-4-bft-threshold dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-4-4-bft-threshold\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-4-4-bft-threshold\target\classes;.\track-06-consensus\task-7-4-4-bft-threshold\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
