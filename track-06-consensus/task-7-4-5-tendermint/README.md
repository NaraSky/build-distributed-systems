# Task 20 - Implement Tendermint-Style BFT Voting Rounds

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-5-tendermint>

Short title: `Tendermint BFT`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-4-5-tendermint dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-4-5-tendermint\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-4-5-tendermint\target\classes;.\track-06-consensus\task-7-4-5-tendermint\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
