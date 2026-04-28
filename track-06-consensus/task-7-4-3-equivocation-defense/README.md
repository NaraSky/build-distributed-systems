# Task 18 - Detect and Handle Equivocation Attacks

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-3-equivocation-defense>

Short title: `Equivocation Defense`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-4-3-equivocation-defense dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-4-3-equivocation-defense\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-4-3-equivocation-defense\target\classes;.\track-06-consensus\task-7-4-3-equivocation-defense\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
