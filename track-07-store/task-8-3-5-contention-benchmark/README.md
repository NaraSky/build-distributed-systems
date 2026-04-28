# Task 15 - Benchmark Contended Key Under OCC vs MVCC

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-3-5-contention-benchmark>

Short title: `Contention Benchmark`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-8-3-5-contention-benchmark dependency:copy-dependencies package
Get-Content .\track-07-store\task-8-3-5-contention-benchmark\samples\input.jsonl | java -cp '.\track-07-store\task-8-3-5-contention-benchmark\target\classes;.\track-07-store\task-8-3-5-contention-benchmark\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
