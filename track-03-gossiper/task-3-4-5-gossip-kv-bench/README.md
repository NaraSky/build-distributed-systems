# Task 20 - Benchmark Gossip KV Store Performance

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-5-gossip-kv-bench>

Short title: `Gossip KV Bench`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-4-5-gossip-kv-bench dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-4-5-gossip-kv-bench\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-4-5-gossip-kv-bench\target\classes;.\track-03-gossiper\task-3-4-5-gossip-kv-bench\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
