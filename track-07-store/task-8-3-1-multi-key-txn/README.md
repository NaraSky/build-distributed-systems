# Task 11 - Implement Multi-Key Transactions as Atomic Log Entries

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-3-1-multi-key-txn>

Short title: `Multi-Key Transactions`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-8-3-1-multi-key-txn dependency:copy-dependencies package
Get-Content .\track-07-store\task-8-3-1-multi-key-txn\samples\input.jsonl | java -cp '.\track-07-store\task-8-3-1-multi-key-txn\target\classes;.\track-07-store\task-8-3-1-multi-key-txn\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
