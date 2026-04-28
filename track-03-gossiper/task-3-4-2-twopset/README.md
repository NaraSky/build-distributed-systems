# Task 17 - Implement Two-Phase Set (2P-Set)

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-2-twopset>

Short title: `2P-Set`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-4-2-twopset dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-4-2-twopset\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-4-2-twopset\target\classes;.\track-03-gossiper\task-3-4-2-twopset\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
