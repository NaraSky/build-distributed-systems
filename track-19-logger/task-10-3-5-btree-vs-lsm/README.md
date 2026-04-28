# Task 15 - Compare B-Tree vs LSM Tree with Amplification Metrics

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-5-btree-vs-lsm>

Short title: `B-Tree vs LSM`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-19-logger/task-10-3-5-btree-vs-lsm dependency:copy-dependencies package
Get-Content .\track-19-logger\task-10-3-5-btree-vs-lsm\samples\input.jsonl | java -cp '.\track-19-logger\task-10-3-5-btree-vs-lsm\target\classes;.\track-19-logger\task-10-3-5-btree-vs-lsm\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
