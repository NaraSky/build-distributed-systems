# Task 18 - Implement Last-Writer-Wins Key-Value Store

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-3-lww-kv>

Short title: `LWW KV Store`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-4-3-lww-kv dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-4-3-lww-kv\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-4-3-lww-kv\target\classes;.\track-03-gossiper\task-3-4-3-lww-kv\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
