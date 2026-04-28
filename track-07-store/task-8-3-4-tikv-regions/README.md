# Task 14 - Build a Mini TiKV with Raft + MVCC Regions

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-3-4-tikv-regions>

Short title: `TiKV Regions`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-8-3-4-tikv-regions dependency:copy-dependencies package
Get-Content .\track-07-store\task-8-3-4-tikv-regions\samples\input.jsonl | java -cp '.\track-07-store\task-8-3-4-tikv-regions\target\classes;.\track-07-store\task-8-3-4-tikv-regions\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
