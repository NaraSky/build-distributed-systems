# Task 15 - Vector Clock Conflict Detection in Key-Value Store

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-5-vc-conflict-kv>

Short title: `VC Conflict KV`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-3-5-vc-conflict-kv dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-3-5-vc-conflict-kv\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-3-5-vc-conflict-kv\target\classes;.\track-02-identifier\task-2-3-5-vc-conflict-kv\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
