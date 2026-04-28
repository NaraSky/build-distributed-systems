# Task 3 - Implement Distributed Cache with Consistent Hashing

Website: <https://builddistributedsystem.com/tracks/caches/tasks/task-11-3-distributed-cache>

Short title: `Distributed Cache`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-11-caches/task-11-3-distributed-cache dependency:copy-dependencies package
Get-Content .\track-11-caches\task-11-3-distributed-cache\samples\input.jsonl | java -cp '.\track-11-caches\task-11-3-distributed-cache\target\classes;.\track-11-caches\task-11-3-distributed-cache\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
