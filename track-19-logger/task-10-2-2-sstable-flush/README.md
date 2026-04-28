# Task 7 - Implement SSTable Flush with Bloom Filter

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-2-sstable-flush>

Short title: `SSTable Flush`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-2-2-sstable-flush dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-2-2-sstable-flush\samples\input.jsonl | java -cp '.\track-19-logger\task-10-2-2-sstable-flush\target\classes;.\track-19-logger\task-10-2-2-sstable-flush\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
