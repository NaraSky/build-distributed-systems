# Task 7 - Implement Lease-Based Reads

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-2-2-lease-reads>

Short title: `Lease Reads`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-8-2-2-lease-reads dependency:copy-dependencies package
Get-Content .\track-07-store\task-8-2-2-lease-reads\samples\input.jsonl | java -cp '.\track-07-store\task-8-2-2-lease-reads\target\classes;.\track-07-store\task-8-2-2-lease-reads\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
