# Task 2 - Add Request Deduplication

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-12-2-dedup>

Short title: `Deduplication`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-12-proxies/task-12-2-dedup dependency:copy-dependencies package
Get-Content .\track-12-proxies\task-12-2-dedup\samples\input.jsonl | java -cp '.\track-12-proxies\task-12-2-dedup\target\classes;.\track-12-proxies\task-12-2-dedup\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
